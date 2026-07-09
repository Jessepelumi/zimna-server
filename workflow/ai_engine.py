import json
from django.utils import timezone
from django.db import transaction
from goals.models import Goal # Goal model
from tasks.models import Task # Task model
from ai.providers.gemini_provider import GeminiProvider
from ai.prompts.goal_decomposition_prompt import DECOMPOSITION_SYSTEM_PROMPT
from conversations.models import Conversation, Message

class YiyaraWorkflow:
    def __init__(self, api_key):
        self.provider = GeminiProvider()

    def create_goals_from_ai(self, user, raw_input):
        """
        The main entry point. Orchestrates AI decomposition and DB persistence.
        """

        # Prepare the dynamic prompt
        full_prompt = f"{DECOMPOSITION_SYSTEM_PROMPT}\n\nUser Input: '{raw_input}'\nCurrent Date: {timezone.now().date()}"

        try:
            # Get structured JSON from the provider
            ai_json_str = self.provider.generate_structured_response(full_prompt)
            ai_response = json.loads(ai_json_str)

            if not isinstance(ai_response, list):
                return [{"error": "ai_format_error", "message": "Expected a list of goals."}]

            # Save to Neon using an atomic transaction
            return self._persist_to_db(user, raw_input, ai_response)

        except Exception as e:
            return [{"error": "workflow_error", "message": str(e)}]

    
    def _persist_to_db(self, user, raw_input, goal_data_list):
        created_goals = []
        
        with transaction.atomic():
            for item in goal_data_list:
                # Create the Goal
                new_goal = Goal.objects.create(
                    user=user,
                    title=item.get('title', 'Untitled Goal'),
                    description=item.get('description', ''),
                    # raw_input helps us track what started this goal
                    raw_input=raw_input, 
                    due_date=item.get('due_date') if item.get('due_date') else None
                )

                # Create associated Tasks
                tasks_to_create = [
                    Task(
                        goal=new_goal,
                        title=t.get('title', 'Untitled Task'),
                        description=t.get('description', '')
                    ) for t in item.get('tasks', [])
                ]
                Task.objects.bulk_create(tasks_to_create)

                created_goals.append(new_goal)
                
            # Associate the conversation with the FIRST goal created for the chat context
            if created_goals:
                primary_goal = created_goals[0]
                conversation, _ = Conversation.objects.get_or_create(goal=primary_goal, user=user)
                Message.objects.create(
                    conversation=conversation,
                    role='model',
                    content=f"I've successfully broken down '{primary_goal.title}' into actionable steps! How would you like to start?"
                )

        return created_goals
    
    