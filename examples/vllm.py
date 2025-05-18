import os
from dotenv import load_dotenv
from vfn_rag.vision.vision_model import VisionModel
load_dotenv()
#%%
image_list = ["examples/data/alge.jpg"]
prompt = """
I have an image of a pond and its surrounding area. Please analyze and describe the ecosystem of the pond in detail.
Focus on identifying visible plant species, types of wildlife, and any signs of ecosystem health, such as water
clarity, presence of algae, and biodiversity indicators. Assess the water quality based on visible factors like
clarity, presence of pollutants, or excessive algae, and discuss whether the pond’s conditions would be suitable
for ducks, geese, fish, and other waterfowl. 
Estimate the pond’s depth based on visual cues (such as the slope of the banks or reflections) and any signs of 
deeper or shallower areas. Additionally, describe the surrounding ecosystem, including visible vegetation types, 
habitat conditions, and potential impacts from human activities, if present. Offer insights into the overall health 
of both the pond and its surrounding ecosystem, and suggest what further
observations could enhance the understanding of the pond's suitability as a habitat for various species and its
ecological health.
"""
#%%
vision_model = VisionModel(image_files=image_list, prompt_template=prompt)
print(vision_model.api_key)
print(vision_model.api_base_url)
print(vision_model.api_version)
#%%
visual_description = vision_model.trigger_model(max_tokens=1000, temperature=0.1, detail="high")
print(visual_description)

#%%
# visual_description = """
# The image depicts a pond surrounded by various types of vegetation and rocks. Here is a detailed analysis of the pond ecosystem based on the visible elements:\n\n### Plant Species\n- **Aquatic Plants**: The pond features water lilies (Nymphaeaceae) with broad, floating leaves and white flowers. These plants are beneficial for providing shade and habitat for aquatic life.\n- **Emergent Vegetation**: There are tall grasses and reeds along the pond's edge, which are typical of wetland environments. These plants help stabilize the pond's banks and provide habitat for wildlife.\n- **Terrestrial Plants**: Surrounding the pond are various shrubs and possibly some low-lying ground cover plants. These contribute to the overall biodiversity and help prevent soil erosion.\n\n### Wildlife\n- **Visible Wildlife**: There are no visible animals in the image, but the presence of water lilies and emergent vegetation suggests that the pond could support various species of insects, amphibians, and possibly small fish.\n- **Potential for Waterfowl**: The pond appears suitable for ducks, geese, and other waterfowl due to the presence of aquatic plants and clear water, which provide food and habitat.\n\n### Water Quality\n- **Clarity**: The water appears clear, indicating good water quality. Clear water is a sign of low pollution levels and a healthy ecosystem.\n- **Algae**: There is no visible excessive algae growth, which suggests that the nutrient levels in the pond are balanced and not overly high.\n- **Pollutants**: There are no visible signs of pollutants such as trash or oil, indicating a relatively clean environment.\n\n### Depth Estimation\n- **Visual Cues**: The pond's depth is difficult to estimate precisely from the image, but the presence of water lilies suggests that at least some parts of the pond are shallow, as these plants typically grow in water up to about 2-3 feet deep.\n- **Bank Slope**: The gentle slope of the banks and the presence of emergent vegetation suggest that the pond may have both shallow and slightly deeper areas.\n\n### Surrounding Ecosystem\n- **Vegetation Types**: The surrounding vegetation includes a mix of grasses, shrubs, and possibly some small trees. This diverse plant life supports a healthy ecosystem by providing habitat and food for various species.\n- **Habitat Conditions**: The habitat appears natural and well-maintained, with no visible signs of human disturbance such as construction or pollution.\n- **Human Impact**: There are no visible signs of significant human impact, which is positive for the overall health of the ecosystem.\n\n### Overall Health and Recommendations\n- **Ecosystem Health**: The pond and its surrounding area appear to be in good health, with clear water, diverse plant life, and no visible pollutants. This suggests a balanced and thriving ecosystem.\n- **Further Observations**: To enhance understanding of the pond's suitability as a habitat and its ecological health, further observations could include:\n  - Monitoring water quality parameters such as pH, dissolved oxygen, and nutrient levels.\n  - Conducting a survey of the wildlife present, including aquatic insects, amphibians, and birds.\n  - Assessing the presence of any invasive species that could impact the native ecosystem.\n\nOverall, the pond appears to be a healthy and suitable habitat for various species, including waterfowl, and contributes positively to the surrounding ecosystem."
# """
