# movie-recommendation
Movie recommendation based on rating scores

## Project Overview
This project consists of 2 parts
1. SVD recommendation modeling
2. Interactive movie recommendation pipeline: user can rate more movies and the pipeline will recommend more movies based on the model prediction values and user's rating scores on each specific movie

## Dataset Overview
source: https://www.kaggle.com/CooperUnion/anime-recommendations-database

### Context
This data set contains information on user preference data from 73,516 users on 12,294 anime. Each user is able to add anime to their completed list and give it a rating and this data set is a compilation of those ratings.

### Content
**Anime.csv**
- `anime_id` - myanimelist.net's unique id identifying an anime.
- `name` - full name of anime.
- `genre` - comma separated list of genres for this anime.
- `type` - movie, TV, OVA, etc.
- `episodes` - how many episodes in this show. (1 if movie).
- `rating` - average rating out of 10 for this anime.
- `members` - number of community members that are in this anime's "group".

**Rating.csv**
- `user_id` - non identifiable randomly generated user id.
- `anime_id` - the anime that this user has rated.
- `rating` - rating out of 10 this user has assigned (-1 if the user watched it but didn't assign a rating).

## How to Run
1. Prepare environment using virtualenv or docker, then install all dependencies listed in `requirements.txt`
2. Download dataset from [kaggle dataset](https://www.kaggle.com/CooperUnion/anime-recommendations-database) to `dataset/anime.csv` and `dataset/rating.csv`
3. SVD model training: run the `model_training.py` script
4. Test model prediction: run the `model_prediction.py` script
5. Run the interactive movie recommendation pipeline: run the `movie_recommendation.py` script