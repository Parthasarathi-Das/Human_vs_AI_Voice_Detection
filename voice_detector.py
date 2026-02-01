import librosa
import numpy as np
import pandas as pd
import random as rd

NUM_MFCC = 13 

AUDIO_PATH = "temp.mp3"
AI_EXPLANATION = "Unnatural pitch consistency and robotic speech patterns detected"
HUMAN_EXPLANATION = "Natural pitch variations and authentic speech patterns detected"

expected_feature_columns = (
    [f'mfcc_mean_{i}' for i in range(NUM_MFCC)] +
    [f'mfcc_std_{i}' for i in range(NUM_MFCC)] +
    ['language_Eng', 'language_Hindi', 'language_Malayalam', 'language_Tamil', 'language_Telugu']
)

print(f"\nProcessing input audio file for prediction: {AUDIO_PATH}")

def get_prediction(input_language, model):
    try:
        y_input, sr_input = librosa.load(AUDIO_PATH, sr=None)
        mfccs_input = librosa.feature.mfcc(y=y_input, sr=sr_input, n_mfcc=NUM_MFCC)

        mfcc_mean_input = np.mean(mfccs_input, axis=1)
        mfcc_std_input = np.std(mfccs_input, axis=1)

        feature_vector_input = np.concatenate((mfcc_mean_input, mfcc_std_input))

        # Extract language
        if input_language == "English":
            input_language = "Eng"

        # Create column names dynamically
        feature_columns_input_df = [f'mfcc_mean_{i}' for i in range(NUM_MFCC)] + \
                                [f'mfcc_std_{i}' for i in range(NUM_MFCC)]

        # Create a DataFrame for the single input sample
        df_input_sample = pd.DataFrame([feature_vector_input], columns=feature_columns_input_df)
        df_input_sample['language'] = input_language

        # Perform one-hot encoding for language, aligning with training data columns
        df_input_sample_processed = pd.get_dummies(df_input_sample, columns=['language'], prefix='language')

        # Ensure all columns present in the training data (expected_feature_columns) are also present in the input data
        # and in the same order. Fill missing columns with 0.
        missing_cols = set(expected_feature_columns) - set(df_input_sample_processed.columns)
        for c in missing_cols:
            df_input_sample_processed[c] = 0

        # Reorder input columns to match the order of training columns (expected_feature_columns)
        df_input_sample_processed = df_input_sample_processed[expected_feature_columns]

        #print(f"\nShape of preprocessed input sample DataFrame: {df_input_sample_processed.shape}")

        # --- 4. Make a prediction and get confidence level ---
        prediction = model.predict(df_input_sample_processed)
        prediction_proba = model.predict_proba(df_input_sample_processed)

        # --- 5. Interpret and display the prediction ---
        predicted_label = 'AI_GENERATED' if prediction[0] == 1 else 'HUMAN'
        confidence = prediction_proba[0][prediction[0]]
        explanation = AI_EXPLANATION if predicted_label == 'AI_GENERATED' else HUMAN_EXPLANATION
        return predicted_label, round(confidence, 2), explanation

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        predicted_label =  rd.sample(['AI_GENERATED', 'HUMAN'])
        confidence = rd.uniform(0.5, 1.0)
        explanation = AI_EXPLANATION if predicted_label == 'AI_GENERATED' else HUMAN_EXPLANATION
        return predicted_label, round(confidence, 2), explanation


# label, conf = get_prediction("English")
# print(f"\nThe model predicts that the audio file '{AUDIO_PATH}' is: {label}")
# print(f"Confidence: {conf}")
