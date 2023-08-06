![CI](https://github.com/dpoulopoulos/forma/workflows/CI/badge.svg)

# Forma
> Automatic format error detection on tabular data.


Forma is an open-source library, written in python, that enables automatic and domain-agnostic format error detection on tabular data. The library is a by-product of the research project [BigDataStack](https://bigdatastack.eu/).

## Install

Run `pip install forma` to install the library in your environment.

## How to use

We will work with the the popular [movielens](https://grouplens.org/datasets/movielens/) dataset.

```python
# local
# load the data
col_names = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_df = pd.read_csv('../data/ratings.dat', delimiter='::', names=col_names, engine='python')
```

```python
# local
ratings_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>movie_id</th>
      <th>rating</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1193</td>
      <td>5</td>
      <td>978300760</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>661</td>
      <td>3</td>
      <td>978302109</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>914</td>
      <td>3</td>
      <td>978301968</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>3408</td>
      <td>4</td>
      <td>978300275</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>2355</td>
      <td>5</td>
      <td>978824291</td>
    </tr>
  </tbody>
</table>
</div>



Let us introduce some random mistakes.

```python
# local
dirty_df = ratings_df.astype('str').copy()

dirty_df.iloc[3]['timestamp'] = '9783000275'
dirty_df.iloc[2]['movie_id'] = '914.'
dirty_df.iloc[4]['rating'] = '10'
```

Initialize the detector, fit and detect. The returned result is a pandas DataFrame with an extra column `p`, which records the probability of a format error being present in the row. We see that the probability for the tuples where we introduced random artificial mistakes is increased.

```python
# local
# initialize detector
detector = FormatDetector()
# fit detector
detector.fit(dirty_df, generator= PatternGenerator(), n=3)
# detect error probability
assessed_df = detector.detect(reduction=np.mean)

# visualize results
assessed_df.head()
```

    100%|██████████| 4/4 [02:58<00:00, 44.58s/it]
    100%|██████████| 1000209/1000209 [07:28<00:00, 2230.59it/s]





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>movie_id</th>
      <th>rating</th>
      <th>timestamp</th>
      <th>p</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1193</td>
      <td>5</td>
      <td>978300760</td>
      <td>0.319957</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>661</td>
      <td>3</td>
      <td>978302109</td>
      <td>0.456679</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>914.</td>
      <td>3</td>
      <td>978301968</td>
      <td>0.509287</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>3408</td>
      <td>4</td>
      <td>9783000275</td>
      <td>0.550982</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>2355</td>
      <td>10</td>
      <td>978824291</td>
      <td>0.569957</td>
    </tr>
  </tbody>
</table>
</div>


