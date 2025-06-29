import os
import json

# Get absolute path to change_log directory relative to this file
CHANGE_LOG_DIR = os.path.join(os.path.dirname(__file__), 'change_log')

def get_available_periods() -> str:
    """
    List all available time periods in the change log directory.
    
    This resource provides a simple list of all available time periods.
    """
    periods = []
    
    # Get all JSON files in the change log directory
    if os.path.exists(CHANGE_LOG_DIR):
        for filename in os.listdir(CHANGE_LOG_DIR):
            if filename.endswith('.json'):
                # Remove .json extension to get period name
                period_name = filename[:-5]
                periods.append(period_name)
    
    # Create a simple markdown list
    content = "# Available Change Log Periods\n\n"
    if periods:
        for period in sorted(periods):
            content += f"- {period}\n"
        content += f"\nUse changelog://<period> to access change logs for that time period.\n"
    else:
        content += "No change log periods found.\n"
    
    return content

def get_period_changelog(period: str) -> str:
    """
    Get detailed information about changes in a specific time period.
    
    Args:
        period: The time period to retrieve change logs for (e.g., "2025_q1" or "2025 Q2")
    """
    # Construct filename directly
    period_filename = period.lower().replace(" ", "_")
    changelog_file = os.path.join(CHANGE_LOG_DIR, f"{period_filename}.json")
    
    if not os.path.exists(changelog_file):
        return f"# No change log found for period: {period}\n\nThe specified time period does not exist or has no recorded changes."
    
    try:
        with open(changelog_file, 'r') as f:
            changelog_data = json.load(f)
        
        # Simple array format: [{"date": "...", "event": "...", "impact": "..."}, ...]
        changes = changelog_data
        content = f"# Change Log for {period.replace('_', ' ').title()}\n\n"
        content += f"Total events: {len(changes)}\n\n"
        
        # Sort changes by date
        sorted_changes = sorted(changes, key=lambda x: x.get('date', ''))
        
        for change in sorted_changes:
            content += f"## {change.get('event', 'Untitled Event')}\n"
            content += f"- **Date**: {change.get('date', 'Unknown')}\n"
            content += f"- **Impact**: {change.get('impact', 'No impact description available.')}\n\n"
            content += "---\n\n"
        
        return content
    except json.JSONDecodeError:
        return f"# Error reading change log data for {period}\n\nThe change log data file is corrupted."
    except Exception as e:
        return f"# Error accessing change log for {period}\n\nError: {str(e)}"