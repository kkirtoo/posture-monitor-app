# --- utils.py ---
# (Placeholder for future utility functions, e.g., smoothing, calibration)

def smooth_angle(angle_list, window=5):
    if len(angle_list) < window:
        return sum(angle_list)/len(angle_list)
    return sum(angle_list[-window:])/window