import json
from google import genai
from google.genai import types
from django.utils import timezone
from django.db import transaction
from goals.models import Goal # Goal model
from tasks.models import Task # Task model

class ZimnaWorkflow:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def process_user_input(self, raw_text):
        model_id = "gemini-3-flash-preview"

        # Schema for the agent to follow strictly
        prompt = f"""
        User Input: "{raw_text}"
        Current Date: {timezone.now().date()}

        Role: You are the Zimna AI Strategic Planner.
        Tasks:
        1. Split the input into individual SMART goals. SMART is short for 'Specific, Measurable, Actionable, Realistic, and Time-bound'.
        2. For each goal, provide a title, a detailed description, and a list of tasks (actionable steps) that must be taken to achieve the goal. Tasks should be specific and actionable, outlining concrete steps to take.
        3. Convert relative dates (like 'Friday' or 'next week') into YYYY-MM-DD. For example, 'next Friday' should be the date of the upcoming Friday (e.g. '2026-03-03').

        Example:
        User Input: "I want to get better at fitness and lose 10 pounds."
        SMARTified Output:
        [
          {{
            "title": "Lose 10 pounds",
            "description": "Lose 10 pounds in 3 months by following a structured workout and diet plan, tracking progress weekly, and achieving a weekly weight loss target.",
            "due_date": "2026-05-23",
            "tasks": [
              {{ "title": "Create fitness plan", "description": "Research and create a balanced fitness plan that includes cardio and strength training." }},
              {{ "title": "Set up diet plan", "description": "Consult with a nutritionist or research online to create a calorie-controlled diet plan." }},
              {{ "title": "Track weight every week", "description": "Weigh yourself once a week on the same day and time to track progress." }},
              {{ "title": "Weekly workout", "description": "Exercise at least 4 times a week following the fitness plan." }},
              {{ "title": "Monitor calories", "description": "Track your daily calorie intake to stay within your target." }}
            ]
          }}
        ]

        Output Format (JSON):
        [
          {{
            "title": "SMART Title",
            "description": "Detailed SMART description",
            "due_date": "YYYY-MM-DD or null",
            "tasks": [
              {{ "title": "Task name", "description": "Short detail" }}
            ]
          }}
        ]

        Notes:
        If the input is unclear or incomplete, ask the user for more details to clarify their goals before proceeding.
        """

        try:
            response = self.client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            data = json.loads(response.text)
            return data if isinstance(data, list) else [{"error": "classification", "message": data}]
            
        except Exception as e:
            return [{"error": "ai_error", "message": str(e)}]
    

    

    def create_goals_from_ai(self, user, raw_input):
        # Get the structured data from Gemini
        ai_response = self.process_user_input(raw_input)

        # If the first item is an error, stop here
        if isinstance(ai_response, list) and len(ai_response) > 0 and "error" in ai_response[0]:
            return ai_response

        created_goals = []

        # Use a transaction to ensure a all-or-nothing saving
        with transaction.atomic():
            for item in ai_response:
                # Create the  New Goal
                new_goal = Goal.objects.create(
                    user = user,
                    title = item.get('title', 'Untitled Goal'),
                    description = item.get('description', ''),
                    raw_input = raw_input,
                    due_date = item.get('due_date') if item.get('due_date') else None
                )

                # Create the associated New Task
                for t_data in item.get('tasks', []):
                    Task.objects.create(
                        goal = new_goal,
                        title = t_data.get('title', 'Untitled Task'),
                        description = t_data.get('description', '')
                    )

                created_goals.append(new_goal)

        return created_goals
    