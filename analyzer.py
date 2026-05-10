import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate_mock_telemetry(records=100):
    start_time = datetime.now()
    data = {
        'timestamp': [start_time + timedelta(seconds=i) for i in range(records)],
        'altitude': np.random.uniform(10, 120, records).tolist(),
        'latitude': [9.02 + (i * 0.0001) for i in range(records)],
        'longitude': [38.74 + (i * 0.0001) for i in range(records)],
        'battery_%': np.linspace(100, 15, records).tolist(),
        'signal_strength': np.random.uniform(70, 95, records).tolist()
    }
    
   
    data['altitude'][50] = 500  # Unauthorized Altitude Spike
    data['latitude'][75] = 12.0  
    
    return pd.DataFrame(data)


class DroneSecurityAnalyzer:
    def __init__(self, df):
        self.df = df
        self.issues = []

    def run_audit(self):
        print("--- Initiating INSA Drone Security Audit ---")
        
        # 1. Check for Altitude Violations (Legal limit is usually 122m / 400ft)
        illegal_alt = self.df[self.df['altitude'] > 122]
        if not illegal_alt.empty:
            self.issues.append(f"ALERT: {len(illegal_alt)} Altitude violations detected!")

        # 2. Check for GPS Spoofing (Sudden distance jumps)
        # We calculate the difference between consecutive GPS points
        self.df['lat_diff'] = self.df['latitude'].diff().abs()
        spoofing_attempts = self.df[self.df['lat_diff'] > 0.1] # 0.1 degree is a massive jump
        if not spoofing_attempts.empty:
            self.issues.append(f"CRITICAL: Potential GPS Spoofing detected at index {spoofing_attempts.index.tolist()}")

        # 3. Check for Battery Safety
        if self.df['battery_%'].iloc[-1] < 20:
            self.issues.append("WARNING: Flight ended with critically low battery (<20%).")

    def generate_report(self):
        print("\n[SECURITY REPORT SUMMARY]")
        if not self.issues:
            print("Status: SECURE. No anomalies detected.")
        else:
            for issue in self.issues:
                print(f"- {issue}")
        
        # Plotting the Altitude for visual proof
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['timestamp'], self.df['altitude'], label='Altitude (m)', color='blue')
        plt.axhline(y=122, color='red', linestyle='--', label='Legal Limit (122m)')
        plt.title('Flight Altitude Security Log')
        plt.xlabel('Time')
        plt.ylabel('Altitude')
        plt.legend()
        plt.show()

# --- STEP 3: EXECUTION ---
if __name__ == "__main__":
    # Generate data
    flight_data = generate_mock_telemetry(100)
    
    # Initialize and Run Analysis
    analyzer = DroneSecurityAnalyzer(flight_data)
    analyzer.run_audit()
    analyzer.generate_report()
