import google.generativeai as genai
import base64
import streamlit as st

genai.configure(api_key=st.secrets['api'])

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash'
)

prompt = f"""
I have used the Windows Battery Report to analyze my laptop's battery performance. Below, I am providing detailed facts and figures, including system information, battery specifications, summaries, and trends from the last 36 hours and daily usage statistics.

I'd like you to analyze the data and provide me with a clear, straightforward summary of your findings. Please keep your explanation simple and easy to understand, as I am not very technical. Focus on answering questions like:

How is my battery performing overall?
Are there any concerning trends I should be aware of?
What insights can I take away from this report about my battery's health and usage patterns?

Important Note: I understand that battery degradation over time is a normal process. However, I would appreciate it if you could provide meaningful and practical suggestions to improve or maintain my battery's performance wherever possible. Avoid technical jargon and focus on actionable insights.

Instructions: Please summarize the key insights from this data and the accompanying plots.
Mention any noteworthy patterns or areas of concern, especially regarding battery health, capacity degradation, or unusual energy consumption trends.
If any trends or metrics seem alarming, explain them in a way I can understand and offer suggestions if relevant and ensure that the response is in markdown format.
keep your explanation simple and easy to understand and in points.
Dont include any headder in the markdown.

Data for Analysis:

"""

def plot_to_base64(buffer):
    """Convert a BytesIO buffer to a Base64 string."""
    if buffer is None:
        return None
    return base64.b64encode(buffer.read()).decode('utf-8')


def summarize_with_ai(summary,base_plots):

    final_promt = prompt+ str(summary)

    query = [final_promt]
    plots = map(plot_to_base64, base_plots)
    query.extend([plot for plot in plots if plot is not None])

    response = model.generate_content(query)

    return response.candidates[0].content.parts[0].text

