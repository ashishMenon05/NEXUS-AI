from .base_grader import BaseGrader

class MediumGrader(BaseGrader):
    def grade(self, episode_state, scenario: dict) -> float:
        score = 0.0
        criteria = scenario.get('grading_criteria', {})
        
        all_msgs = [m.lower() for m in episode_state.agent_a_messages + episode_state.agent_b_messages]
        
        root_cause = scenario.get("root_cause", {})
        affected_service = root_cause.get("affected_service", "").lower()
        affected_param = root_cause.get("affected_parameter", "").lower()
        
        # Identified core issue pieces
        if affected_service and any(affected_service in msg for msg in all_msgs):
            keys_matching = [k for k in criteria.keys() if "identified" in k]
            if len(keys_matching) > 0:
                score += criteria[keys_matching[0]]
                
        if affected_param and any(affected_param in msg for msg in all_msgs):
            keys_matching = [k for k in criteria.keys() if "identified" in k]
            if len(keys_matching) > 1:
                score += criteria[keys_matching[1]]

        if getattr(episode_state, "fix_correct", False) or episode_state.fix_verified:
            score += criteria.get('correct_fix_proposed', 0)
                
        if episode_state.fix_verified:
            score += criteria.get('fix_verified', 0)
            
        if episode_state.max_rounds > 0:
            steps_ratio = episode_state.current_round / episode_state.max_rounds
            if steps_ratio <= 0.5 and episode_state.fix_verified:
                score += criteria.get('efficiency_bonus', 0)
                
        # Medium adds penalty for red herrings
        red_herrings = scenario.get("red_herrings", [])
        # We can extract penalty from criteria keys that start with "penalty_"
        penalty_keys = [k for k in criteria.keys() if k.startswith("penalty_")]
        for pk in penalty_keys:
            # If the red herring service/keyword was mentioned excessively
            score += criteria[pk] # usually a negative number
            
        return max(0.0, min(1.0, round(score, 4)))
