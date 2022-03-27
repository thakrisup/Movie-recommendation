import pandas as pd


def create_dataset(rating_csv_path: str):
    """Preprocess the dataset from CSV path
    Parameter
    - rating_csv_path       : string
                            : path to the CSV file which store the user-rating information
    Return
    - filtered_rating       : pd.DataFrame
                            : relation data between rating score for selected users on selected movies
    - filtered_rating_2     : pd.DataFrame
                            : relation data between rating score for selected users on selected movies (including watched movies)
    note: `-1` rating score is when the user watched the movie but didn't assign a rating
    """
    df_rating = pd.read_csv(rating_csv_path)
    df_rating_2 = df_rating[df_rating["rating"]!=-1]  # `-1` is when the user watched the movie but didn't assign a rating

    # select qualified movie id
    movie_rating_count = df_rating_2.groupby(by='anime_id').count()['rating'].reset_index().rename(columns={'rating':'rating_count'})
    movie_rating_count.head()

    # select qualified user_id
    user_rating_count = df_rating_2.groupby(by='user_id').count()['rating'].reset_index().rename(columns={'rating':'rating_count'})
    user_rating_count.head()

    # filter-out some data in the `df_rating`
    filtered_movie = movie_rating_count[movie_rating_count['rating_count']>250]
    filtered_user = user_rating_count[user_rating_count['rating_count']>100]
    filtered_rating_movie = df_rating_2[df_rating_2['anime_id'].isin(filtered_movie['anime_id'])]
    filtered_rating = filtered_rating_movie[filtered_rating_movie['user_id'].isin(filtered_user['user_id'])]
    filtered_rating = filtered_rating.rename(columns={'user_id': 'user', 'anime_id': 'item'})

    # filter-out some data in the `df_rating` (included watched movies)
    filtered_rating_movie_watched = df_rating[df_rating['anime_id'].isin(filtered_movie['anime_id'])]
    filtered_rating_watched = filtered_rating_movie_watched[filtered_rating_movie_watched['user_id'].isin(filtered_user['user_id'])]
    filtered_rating_watched = filtered_rating_watched.rename(columns={'user_id': 'user', 'anime_id': 'item'})

    return filtered_rating, filtered_rating_watched


def create_matrix_dataset(rating_csv_path):
    filtered_rating, filtered_rating_watched = create_dataset(rating_csv_path)
    rating_matrix = filtered_rating.pivot_table(index='user',columns='item',values='rating')
    rating_matrix_watched = filtered_rating_watched.pivot_table(index='user',columns='item',values='rating')
    rating_matrix_watched = rating_matrix_watched.notnull().astype('int')
    return rating_matrix, rating_matrix_watched


def validate_user_id(df_filtered_rating, user_id):
    _df = df_filtered_rating[df_filtered_rating['user']==user_id]
    return len(_df) > 0

def validate_movie_id(df_filtered_rating, movie_id):
    _df = df_filtered_rating[df_filtered_rating['item']==movie_id]
    return len(_df) > 0

def get_user_movie_list(df_filtered_rating):
    _df_item = df_filtered_rating.groupby('item').agg({
        'item': 'first'
    })
    item_list = _df_item['item'].tolist()

    _df_user = df_filtered_rating.groupby('user').agg({
        'user': 'first'
    })
    user_list = _df_user['user'].tolist()
    return item_list, user_list
