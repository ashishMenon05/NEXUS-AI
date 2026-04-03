from .base_grader import BaseGrader

class HardGrader(BaseGrader):
    def grade(self, episode_state, scenario: dict) -> float:
        score = 0.0
        criteria = scenario.get('grading_criteria', {})
        
        all_msgs = [m.lower() for m in episode_state.agent_a_messages + episode_state.agent_b_messages]
        
        # Hard grader adds cascade order correctness scoring and prevention plan checking
        root_cause = scenario.get("root_cause", {})
        affected_service = root_cause.get("affected_service", "").lower()
        affected_param = root_cause.get("affected_parameter", "").lower()
        
        keys_matching_ident = [k for k in criteria.keys() if "identified" in k]
        
        if affected_service and any(affected_service in msg for msg in all_msgs):
            if len(keys_matching_ident) > 0:
                score += criteria[keys_matching_ident[0]]
                
        if affected_param and any(affected_param in msg for msg in all_msgs):
            if len(keys_matching_ident) > 1:
                score += criteria[keys_matching_ident[1]]
                
        if getattr(episode_state, "fix_correct", False) or episode_state.fix_verified:
            if "ordered_fix_proposed" in criteria:
                score += criteria.get("ordered_fix_proposed", 0)
            else:
                score += criteria.get('correct_fix_proposed', 0)
                
        if episode_state.fix_verified:
            score += criteria.get('fix_verified', 0)
            
        if episode_state.max_rounds > 0:
            steps_ratio = episode_state.current_round / episode_state.max_rounds
            if steps_ratio <= 0.5 and episode_state.fix_verified:
                score += criteria.get('efficiency_bonus', 0)
                
        if "prevention_plan_mentioned" in criteria:
            if any(term in msg for msg in all_msgs for term in ["prevent", "avoid in future", "add alert", "plan", "safeguard"]):
                score += criteria["prevention_plan_mentioned"]

        if "recalculation_step_mentioned" in criteria:
            if any(term in msg for msg in all_msgs for term in ["recalculate", "backfill", "recompute"]):
                score += criteria["recalculation_step_mentioned"]
                
        return max(0.0, min(1.0, round(score, 4)))
