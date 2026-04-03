from .base_grader import BaseGrader

class EasyGrader(BaseGrader):
    def grade(self, episode_state, scenario: dict) -> float:
        score = 0.0
        criteria = scenario.get('grading_criteria', {})
        
        all_msgs = [m.lower() for m in episode_state.agent_a_messages + episode_state.agent_b_messages]
        
        root_cause = scenario.get("root_cause", {})
        affected_service = root_cause.get("affected_service", "").lower()
        affected_param = root_cause.get("affected_parameter", "").lower()
        
        # 1. Identified affected service
        if affected_service and any(affected_service in msg for msg in all_msgs):
            # Try to get points by the criteria keys dynamically, or default to some fraction
            for k, v in criteria.items():
                if "service" in k or affected_service in k or k.startswith("identified_"):
                    score += v
                    break
        
        # 2. Identified parameter
        if affected_param and any(affected_param in msg for msg in all_msgs):
            for k, v in criteria.items():
                if ("parameter" in k or affected_param in k) and k != "identified_redis": # arbitrary checks
                    score += v
                    break
                    
        # 3. Fixed proposed
        if episode_state.fix_proposed: # Assuming episode state marks if it was correct
            # In our system, if it's correct, fix_verified might be True
            if getattr(episode_state, "fix_correct", False) or episode_state.fix_verified:
                score += criteria.get('correct_fix_proposed', 0)
                
        # 4. Fix Verified
        if episode_state.fix_verified:
            score += criteria.get('fix_verified', 0)
            
        # 5. Efficiency Bonus
        if episode_state.max_rounds > 0:
            steps_ratio = episode_state.current_round / episode_state.max_rounds
            if steps_ratio <= 0.5 and episode_state.fix_verified:
                score += criteria.get('efficiency_bonus', 0)
                
        return min(1.0, round(score, 4))
