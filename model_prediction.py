import pickle
import pandas as pd
from utils.data_prep import create_dataset, validate_user_id, validate_movie_id, get_user_movie_list


model_path = 'models/svd_2022-03-26T04:12:44+07:00.model'
movie_csv_path = 'dataset/anime.csv'
rating_csv_path = 'dataset/rating.csv'
user_id = 5

df_movie = pd.read_csv(movie_csv_path)

# load model
loaded_svd = pickle.load(open(model_path, 'rb'))

# prepare dataset
filtered_rating, _ = create_dataset(rating_csv_path)

# show amount of available user_id and movie_id
item_list, user_list = get_user_movie_list(filtered_rating)
print('movie amount: ', item_list)
print('user amount: ', user_list)

# model prediction demo
if validate_user_id(filtered_rating, user_id):
    # model prediction
    preds = loaded_svd.predict_for_user(user_id, item_list)

    # change predicted pd.Series to pd.DataFrame
    df_preds = preds.to_frame(name="rating_preds").reset_index()
    df_preds = df_preds.rename(columns={"index": "anime_id"})

    # select the top 10 largest prediction rating values
    df_preds_top10 = df_preds.nlargest(10, "rating_preds")
    df_preds_top10 = pd.merge(df_preds_top10, df_movie, on=["anime_id"])

    print('recommended movies (Top 10)')
    print(df_preds_top10)

else:
    raise Exception('invalid `user_id` input, please try again')
