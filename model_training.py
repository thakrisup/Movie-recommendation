import pickle
import pendulum
import lenskit.algorithms.svd as SVD
from utils.data_prep import create_dataset


movie_csv_path = 'dataset/anime.csv'
rating_csv_path = 'dataset/rating.csv'
model_directory = 'models'

# prepare dataset
filtered_rating, _ = create_dataset(rating_csv_path)

# model training
print('start training SVD model')
svd = SVD.BiasedSVD(features=1000)
svd.fit(filtered_rating)

# save model to local directory
_now = pendulum.now(tz='Asia/Bangkok')
dt_string = _now.to_atom_string().replace(":", "_")
filename = f'{model_directory}/svd_{dt_string}.model'
pickle.dump(svd, open(filename, 'wb'))
print(f'saved SVD model to {filename}')
