import pickle
import random
from tabulate import tabulate
import pandas as pd
import numpy as np
from utils.data_prep import create_dataset, validate_user_id, validate_movie_id, get_user_movie_list, create_matrix_dataset


def print_df(df):
    """displaying DataFrame"""
    print(tabulate(df, headers = 'keys', tablefmt = 'pretty'))


def input_user_id(user_list):
    while True:
        try:
            print("\navailable user_id from dataset (random) : {}".format(random.sample(user_list, 5)))
            user_id = int(input())
            if (user_id in user_list):
                print("The selected user_id is {}".format(user_id))
                break
            else:
                print("the selected user_id is not available")
                continue
        except:
            print("incorrect format, please try again")
            continue
    return user_id


def input_continue():
    while True:
        print("Do you what to watch more movie ? (y/n)")
        ans = str(input())
        if (ans.lower()[0] == "y"):
            ans = "y"
            break
        elif (ans.lower()[0] == "n"):
            ans = "n"
            break
        else:
            print("Invalid input, please try again\n")
            continue
    return ans


def input_item_id(watched_movie):
    while True:
        try:
            item_list_temp = [item for item in item_list if item not in watched_movie]
            print("\navailable item_id from dataset (random) : {}".format(random.sample(item_list_temp, 5)))
            item_id = int(input())
            if (item_id in item_list_temp):
                print("The selected item_id is {}\n".format(item_id))
                break
            else:
                print("the selected item_id is not available\n")
                continue
        except:
            print("incorrect format, please try again\n")
            continue
    return item_id


def input_rate():
    while True:
        try:
            print("rate the movie (rate 1-10, -1 is not rate)")
            rate = int(input())
            if (rate in rate_list):
                print("The selected rate is {}\n".format(rate))
                break
            else:
                print("the selected rate is not available\n")
                break
        except:
            print("incorrect format, please try again\n")
            break
    return rate


def compute_preds_100(preds, watched_movie, df_movie):
    df_preds = preds.to_frame(name="rating_preds").reset_index()
    df_preds = df_preds.rename(columns={"index": "anime_id"})
    df_preds = df_preds[~df_preds.anime_id.isin(watched_movie)]
    df_movie_2 = df_movie.drop(columns=["rating", "members", "episodes"])
    df_preds = pd.merge(df_preds, df_movie_2, on=["anime_id"])
    df_preds_100 = df_preds.nlargest(100, "rating_preds")
    return df_preds, df_preds_100


def compute_genres_weight(df_preds):
    genre_set = set()
    df_movie_genres = df_preds["genre"].fillna("")
    for genre in df_movie_genres.iloc[:]:
        genre_list = genre.split(", ")
        for g in genre_list:
            genre_set.add(g)
    if ("" in genre_set):
        genre_set.remove("")
    genre_dict = {
            "genre" : list(genre_set),
            "weight" : np.zeros(len(genre_set))
        }
    df_genres_weight = pd.DataFrame(genre_dict)
    return df_genres_weight


def get_rate_pred(item_id, df_preds):
    try:
        return df_preds[df_preds.anime_id == item_id].rating_preds.values[0]
    except:
        return -1


def update_genres_weight(item_id, df_preds, df_genres_weight, value, direction):
    genre_str = df_preds[df_preds.anime_id == item_id].genre.values[0]
    genre_list = genre_str.split(", ")
    if (direction == "up"):
        for genre in genre_list:
            df_genres_weight.loc[df_genres_weight.genre == genre, "weight"] += value
    elif (direction == "down"):
        for genre in genre_list:
            df_genres_weight.loc[df_genres_weight.genre == genre, "weight"] -= value
    return df_genres_weight


def update_preds_100(df_preds, df_genres_weight, df_movie, first_iter=False):
    if (first_iter):
        df_preds["avg_weight"] = np.zeros(len(df_preds))
        df_preds["score"] = np.zeros(len(df_preds))
        column_names = ["anime_id", "score", "avg_weight", "name", "genre", "rating_preds", "type"]
        df_preds = df_preds.reindex(columns=column_names)
    for i in range(len(df_preds)):
        genres = df_preds.iloc[i].genre
        if (len(genres)>0):
            genre_list = genres.split(", ")
            weights = []
            for genre in genre_list:
                weight = df_genres_weight[df_genres_weight.genre == genre]["weight"].values[0]
                weights.append(weight)
            df_preds.iloc[i, df_preds.columns.get_loc("avg_weight")] = sum(weights) / len(weights)
    df_preds["score"] = df_preds["rating_preds"] + df_preds["avg_weight"]
    df_preds = df_preds[~df_preds.anime_id.isin(df_movie)]
    df_preds_100 = df_preds.nlargest(100, "score")
    return df_preds, df_preds_100 


def get_watched_movie(user_id, df_movie_watched):
    df = df_movie_watched.iloc[df_movie_watched.index == user_id]
    columns = list(df.columns)
    values = df.values.tolist()[0]
    watched_list = []
    for c, v in zip(columns, values):
        if (v==1):
            watched_list.append(c)
    return watched_list


if __name__ == '__main__':
    model_path = 'models/svd_2022-03-26T14_53_13+07_00.model'
    movie_csv_path = 'dataset/anime.csv'
    rating_csv_path = 'dataset/rating.csv'
    user_id = 5

    df_movie = pd.read_csv(movie_csv_path)

    # load model
    loaded_svd = pickle.load(open(model_path, 'rb'))

    # prepare dataset
    filtered_rating, _ = create_dataset(rating_csv_path)
    rating_matrix, rating_matrix_watched = create_matrix_dataset(rating_csv_path)

    # get filtered user_id and item_id
    item_list, user_list = get_user_movie_list(filtered_rating)

    rate_list = [-1]+list(range(1, 11))

    step = 1

    break_line = "\n----------\n"

    # Pipeline
    print("Start the Program ...")
    print(break_line)
    print("({}) Select a user_id : ".format(step))
    step += 1

    user_id = input_user_id(user_list)
    watched_anime = get_watched_movie(user_id, rating_matrix_watched)
    print("amount of anime watched : ", len(watched_anime))

    print(break_line)
    print("({}) Make recommendation for user_id : {}\n".format(step, user_id))
    step += 1

    preds = loaded_svd.predict_for_user(user_id, item_list)
    df_preds, df_preds_100 = compute_preds_100(preds, watched_anime, df_movie)

    df_preds_10 = df_preds_100.iloc[:10]
    print_df(df_preds_10)

    df_genres_weight = compute_genres_weight(df_preds)
    print_df(df_genres_weight[df_genres_weight.weight!=0])

    print(break_line)
    print("({}) Make recommendation from what the user rated\n".format(step))

    first_iter = True

    while True:
        ans = input_continue()

        if (ans == "n"):
            print("Close the Program")
            break

        elif (ans == "y"):
            sub_step = 1
            print("\n({}-{}) Select an item_id : ".format(step, sub_step))
            sub_step += 1
            
            item_id = input_item_id(watched_anime)
            watched_anime.append(item_id)

            print("({}-{}) Rate movie-{} : \n".format(step, sub_step, item_id))
            sub_step += 1
            
            rate_input = input_rate()

            print("Processing new recommendataion ...\n")

            rate_pred = get_rate_pred(item_id, df_preds)

            if (rate_pred == -1):
                print("user have already watched this movie, try other movie_id")
            
            else:
                if (rate_input == -1):
                    pass
                elif (rate_input >= rate_pred):
                    print("increment genre weights")
                    df_genres_weight = update_genres_weight(item_id, df_preds, df_genres_weight, 0.5, direction="up")
                else:
                    print("decrement genre weights")
                    df_genres_weight = update_genres_weight(item_id, df_preds, df_genres_weight, 0.5, direction="down")

                print_df(df_genres_weight[df_genres_weight.weight!=0])

                df_preds, df_preds_100 = update_preds_100(df_preds, df_genres_weight, watched_anime, first_iter=first_iter)
                first_iter = False

                df_preds_10 = df_preds_100.iloc[:10]
                print_df(df_preds_10)

            print(break_line)

            step += 1
