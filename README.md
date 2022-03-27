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

## Interactive Movie Recommendation's System Diagram
![Movie Recommendation Pipeline](https://user-images.githubusercontent.com/93319372/160292160-5ac04ce7-79a8-4bf5-a61f-0b35eb33ecea.jpeg)


## Interactive Movie Recommendation's Output Example
The pipeline will ask the user to select the user_id to play as this person, then it will perform SVD model prediction to predict the estimated rating score on all unseen movies and suggest a initial movie set to the user
![image_1](https://user-images.githubusercontent.com/93319372/160292166-c7048e1c-ef88-4511-bb4e-121e703c9b89.png)

The pipeline will ask whether the user want to continue watching the movie and rate the selected movie. In this case, I choose movie_id 28977 which include Comedy genre and rate it with 9. The pipeline will adjust the genre-weights for each genre-type included in movie_id 28977 and suggest to the user again.
![image_2](https://user-images.githubusercontent.com/93319372/160292168-6f6c967b-32f5-43c3-acca-d206334fc65f.png)

I continue choosing movie_id 9863 which include Comedy genre and rate it with 8. The pipeline will adjust the genre-weights for each genre-type included in movie_id 9863 and suggest to the user again.
![image_3](https://user-images.githubusercontent.com/93319372/160292170-561956aa-76d3-41f2-9385-b3393db577fe.png)

I continue choosing movie_id 5114 which include Action genre and rate it with 3. The pipeline will adjust the genre-weights for each genre-type included in movie_id 5114 and suggest to the user again.
![image_4](https://user-images.githubusercontent.com/93319372/160292184-b387993b-a632-4872-85f9-96f7889f9eaa.png)

After selecting and rating movies continuously with the goal of giving Comedy genre movies good rating scores and Action genre movies bad rating scores, the pipeline have continuously adjust the genre-weights and suggest a movie set that mostly include Comedy genre and neglecting Action genre to the user.
![image_5](https://user-images.githubusercontent.com/93319372/160292194-a2d7e866-29c9-4c1a-9f7e-bb6338029e1a.png)
