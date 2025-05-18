from typing import List, Union
from pathlib import Path
import os
import base64
import cv2
import numpy as np
from openai import AzureOpenAI
from llama_index import __path__
from vfn_rag.vision.utils import load_yaml_key_value


class VisionModel:

    def __init__(
        self,
        image_files: List[str] = None,
        image_dir: str = None,
        prompt_template: str = None,
        vllm: AzureOpenAI = None,
    ):
        """
        Parameters
        ----------
        image_files : List[str]
            A list of image files.
        image_dir: str
            The directory containing the image files.
        prompt_template : str, optional, default is None.
            The path to the YAML file containing the prompt template. if none is given the default prompt will be
            loaded from the package.

        Raises
        ------
        FileNotFoundError
            If the directory is not found.
        """
        if isinstance(image_files, list):
            self._images = image_files
        elif isinstance(image_dir, str):
            if not Path(image_dir).exists():
                raise FileNotFoundError(f"Directory {image_dir} not found.")

            self._images = list(Path(image_dir).iterdir())
        else:
            raise ValueError(
                "Please provide a list of image files or a directory path."
            )

        self._load_api_keys()
        if vllm is None:
            self._mm_llm = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                base_url=f"{self.api_base_url}/deployments/{self.deployment_name}",
            )
        else:
            self._mm_llm = vllm

        if prompt_template is None:
            self._prompt_template = self.load_prompt()
        else:
            self._prompt_template = prompt_template

    @property
    def mm_llm(self) -> AzureOpenAI:
        return self._mm_llm

    @mm_llm.setter
    def mm_llm(self, value: AzureOpenAI):
        self._mm_llm = value

    @property
    def prompt_template(self):
        return self._prompt_template

    def _load_api_keys(self):
        self.api_version = "2024-03-01-preview"
        self.api_base_url = os.getenv("OPENAI_API_BASE")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    @prompt_template.setter
    def prompt_template(self, value: str):
        self._prompt_template = value

    @property
    def images(self) -> List[str]:
        return self._images

    @staticmethod
    def encode_image(image: np.ndarray, image_format: str = "jpeg") -> str:
        """Encodes an OpenCV image to a Base64 string.

        Parameters
        ----------
        image (np.ndarray): An image represented as a numpy array.
        format (str, optional): The format for encoding the image. Defaults to 'jpeg'.

        Returns
        -------
        str:
            A Base64 encoded string of the image.

        Raises
        ------
        ValueError:
            If the image conversion fails.
        """
        try:
            retval, buffer = cv2.imencode(f".{image_format}", image)
            if not retval:
                raise ValueError("Failed to convert image")

            base64_encoded = base64.b64encode(buffer).decode("utf-8")
            mime_type = f"image/{image_format}"
        except Exception as e:
            raise ValueError(f"Error encoding image: {e}")

        return f"data:{mime_type};base64,{base64_encoded}"

    def encode_images(self) -> List[str]:
        """Encodes a list of images to Base64 strings.

        Returns
        -------
        List[str]:
            A list of Base64 encoded strings of the images.

        Examples
        --------
        ```python
        >>> model = VisionModel(image_dir="images")
        >>> images = model.encode_images()
        >>> print(images[0])
        'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEB.....
        ```
        """
        img_encoded = []
        for img in self.images:
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_encoded.append(self.encode_image(img))

        return img_encoded

    def trigger_model(self, max_tokens=3000, temperature=0.8, detail="high"):
        """Triggers the Azure OpenAI model with the images.

        Parameters
        ----------
        max_tokens : int, optional, default is 1000.
            The maximum number of tokens to generate.
        temperature : float, optional, default is 0.1.
            The sampling temperature.
        detail : str, optional, default is "high".
            The detail level of the response.

        Returns
        -------
        str:
            The response from the model.

        Examples
        --------
        ```python
        >>> model = VisionModel(image_dir="images")
        >>> response = model.trigger_model(max_tokens=1000, temperature=0.1, detail="high")
        >>> print(response)
        ```
        """
        img_encoded = self.encode_images()
        message = create_message(img_encoded, detail)
        response = self.mm_llm.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": f"{self.prompt_template}"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{self.prompt_template}"},
                        *message,
                    ],
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        content = response.choices[0].message.content
        self._response = content
        return content

    @property
    def response(self) -> Union[str, None]:
        if self._response:
            return self._response
        else:
            return None

    def to_markdown(self, path: str = "sample.md"):
        """Writes the output to a markdown file.

        Parameters
        ----------
        path : str, optional, default is "sample.md".
            The path to save the markdown file.

        Raises
        ------
        ValueError
            If no response is available.

        Examples
        --------
        ```python
        >>> model = VisionModel(image_dir="images")
        >>> response = model.trigger_model(max_tokens=1000, temperature=0.1, detail="high")
        >>> model.to_markdown("sample.md")
        ```
        """
        if self.response is None:
            raise ValueError("No response available.")

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        header = f"# Fact sheet - polygon: {path}\n## Description Agent 1\n"
        full_text = header + self.response
        file_path.write_text(full_text, encoding="utf-8")

    @staticmethod
    def load_prompt(path: str = None, key: str = "vision model") -> str:
        """Load the prompt template from a YAML file.

        Parameters
        ----------
        path : str, optional, default is None.
            The path to the YAML file.
        key : str, optional, default is "vision_model".
            The key to retrieve the prompt.

        Returns
        -------
        str:
            The prompt template.

        Raises
        ------
        FileNotFoundError
            If the file is not found.

        Examples
        --------
        ```python
        path = "path/to/prompt.yaml"
        key = "vision_model"
        >>> template = load_prompt(path, key)
        >>> print(template)
        ```
        """
        if path is None:
            path = os.path.join(__path__[0], "prompt.yaml")

        content = load_yaml_key_value(path, key)

        return content

def create_message(image_list: List[str], detail: str = "high") -> List[dict]:
    image_messages = [
        {
            "type": "image_url",
            "image_url": {
                "url": img,
                "detail": detail,
            },
        }
        for img in image_list
    ]
    return image_messages
