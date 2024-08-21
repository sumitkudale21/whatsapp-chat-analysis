import re
import pandas as pd

def preprocess(data):
    # Regular expression to extract date, time, sender, and message for WhatsApp chat data
    pattern_v2 = r'^(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2} [apAP][mM]) - ([^:]+): (.*)$'

    # Lists to store extracted data
    dates = []
    times = []
    senders = []
    messages = []

    # Initialize a variable to keep track of the previous message if needed
    current_message = ""

    # Parse each line in the chat data
    for line in data:
        line = line.strip()
        match = re.match(pattern_v2, line)
        if match:
            if current_message:  # If there's an ongoing message, append it
                messages.append(current_message)
                current_message = ""

            dates.append(match.group(1))
            times.append(match.group(2))
            senders.append(match.group(3))
            messages.append(match.group(4))
        else:
            # If the line doesn't match the pattern, it might be a continuation of the previous message
            if messages:
                current_message += ' ' + line

    # Append the last message if any
    if current_message:
        messages.append(current_message)

    # Print lengths for debugging
    print(f"Dates length: {len(dates)}")
    print(f"Times length: {len(times)}")
    print(f"Senders length: {len(senders)}")
    print(f"Messages length: {len(messages)}")

    # Ensure all lists are of the same length
    min_length = min(len(dates), len(times), len(senders), len(messages))
    dates = dates[:min_length]
    times = times[:min_length]
    senders = senders[:min_length]
    messages = messages[:min_length]

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Sender': senders,
        'Message': messages
    })

    # Convert 'Date' to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    # Combine 'Date' and 'Time' into a single 'DateTime' column
    df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'])

    # Extract additional time-based columns
    df['Day'] = df['DateTime'].dt.day
    df['Month'] = df['DateTime'].dt.month
    df['Year'] = df['DateTime'].dt.year
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute
    
    # Optionally, drop the original 'Date' and 'Time' columns if only 'DateTime' is needed
    df.drop(['Date', 'Time'], axis=1, inplace=True)

    return df
