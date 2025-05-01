import requests
from .prompts import refine_idea_prompt, lean_canvas_prompt, mvp_blueprint_prompt

API_URL = "https://api.together.ai/v1/models/mistral-7b-instruct-v0.1"

def call_api(prompt):
    response = requests.post(API_URL, json={"prompt": prompt})
    return response.json().get('output', '')

def generate_outputs(idea):
    refined_idea = call_api(refine_idea_prompt(idea))
    lean_canvas = call_api(lean_canvas_prompt(refined_idea))
    mvp_blueprint = call_api(mvp_blueprint_prompt(refined_idea))
    
    return f"Refined Idea:\n{refined_idea}\n\nLean Canvas:\n{lean_canvas}\n\nMVP Blueprint:\n{mvp_blueprint}"