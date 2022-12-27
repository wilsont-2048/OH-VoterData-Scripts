import pandas as pd
import re


def read_data():
    # List to store individual DataFrames.
    frames = []

    print("Reading data...")

    # Place county data into a DataFrame and append to list.
    for i in range(1, 5):
        frames.append(pd.read_csv(f'./DATA/data{i}.txt'))

    print("Process complete.")

    # Consolidate all DataFrames into one main DataFrame.
    df = pd.concat(frames, ignore_index=True)

    # Removing unecessary columns on DataFrame.
    df = df[["SOS_VOTERID", "LAST_NAME", "FIRST_NAME",
                 "MIDDLE_NAME", "DATE_OF_BIRTH", "RESIDENTIAL_ADDRESS1", 
                 "RESIDENTIAL_SECONDARY_ADDR", "RESIDENTIAL_CITY", 
                 "RESIDENTIAL_STATE", "RESIDENTIAL_ZIP"]]

    return df


def format_data(data):
    print("Cleaning up data...")

    # Adding a column for full residential address.
    data["address"] = data[["RESIDENTIAL_ADDRESS1", "RESIDENTIAL_SECONDARY_ADDR"]].fillna("").astype(str).apply(lambda x: re.sub(" +", " ", " ".join(x)), axis=1).str.title()

    # Adding a column for birth year only from date of birth.
    data["birth_year"] = data["DATE_OF_BIRTH"].str.split("-").str[0]
    data["birth_year"] = data["birth_year"].astype(float)

    # Further format data columns.
    data["zip"] = data["RESIDENTIAL_ZIP"].astype(float)
    data["city"] = data["RESIDENTIAL_CITY"].str.title()
    data.rename(columns= {"RESIDENTIAL_STATE":"state"}, inplace=True)
    data.rename(columns= {"SOS_VOTERID":"voterid"}, inplace=True)

    print("Process complete.")

    return data


def match_data(data):
    # Get data to match from input csv file at root user folder.
    input_data_df = pd.read_csv('./eng-matching-input-v3.csv')
    input_data_df.fillna("", inplace=True)

    # Format data columns to be used.
    input_data_df["FIRST_NAME"] = input_data_df["name"].str.split().str[0].str.upper()
    input_data_df["LAST_NAME"] = input_data_df["name"].str.split().str[-1].str.upper()

    # Merge both DataFrames by inner join on "LAST_NAME".
    temp_df = pd.merge(input_data_df, data, on=["LAST_NAME"], how="inner")
    temp_df = temp_df.fillna("")

    print("Matching data...")

    # Further narrow results by selecting rows with equal values at "FIRST_NAME".
    temp_df = temp_df[(temp_df.FIRST_NAME_x == temp_df.FIRST_NAME_y)]

    # Further narrow results by selecting rows with equal values at zip or birth year.
    final_df = temp_df[(temp_df.zip_x == temp_df.zip_y) | (temp_df.birth_year_x == temp_df.birth_year_y)]

    print("Process complete.")

    # Clean up final DataFrame to include only needed columns.
    final_df = final_df[["row", "name", "birth_year_x", "address_x", "city_x", "state_x", "zip_x", "voterid"]]
    final_df.rename(columns={"birth_year_x":"birth_year", "address_x":"address", "city_x":"city", "state_x":"state", "zip_x":"zip", "voterid":"matched_voterid"}, inplace=True)
    final_df = final_df.sort_values(by=["row"])
    final_df["birth_year"] = final_df["birth_year"].astype(str).str.split('.').str[0]
    final_df["zip"] = final_df["zip"].astype(str).str.split('.').str[0]

    return final_df


def write_data(data):
    print("Writing final data to file...")

    data.to_csv("matched_data.csv", index=False)

    print("Process complete.")


def main():
    temp_data = read_data()
    data = format_data(temp_data)
    result = match_data(data)

    write_data(result)


if __name__ == '__main__':
    main()
