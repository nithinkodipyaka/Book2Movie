const dfd = require("danfojs-node");
const math = require("mathjs");
const path = require('path');
const fs = require('fs');

async function loadData() {
    const moviesPath = path.join(__dirname, '../Dataset/movies/movies_metadata.csv');
    const keywordsPath = path.join(__dirname, '../Dataset/movies/keywords.csv');

    let movies = await dfd.readCSV(moviesPath);
    let keywords = await dfd.readCSV(keywordsPath);

    // Process genres column
    movies['genres'] = movies['genres'].apply(genres => {
        if (!genres) return [];
        genres = JSON.parse(genres);
        return genres.map(genre => genre.name);
    });

    movies['id'] = movies['id'].apply(id => (typeof id === 'string' && id.match(/^\d+$/)) ? parseInt(id) : null);
    movies = movies.dropna({ 'id': true });
    keywords['id'] = keywords['id'].astype('int');

    movies = await movies.merge(keywords, { on: 'id' });

    movies['keywords'] = movies['keywords'].apply(keywords => JSON.parse(keywords));
    
    return movies;
}

exports.recommend = async (req, res) => {
    const bookName = req.body.book_name;

    let movies;
    try {
        movies = await loadData();
    } catch (err) {
        return res.status(500).send("Error loading data");
    }

    // Implement recommendation logic here...
    let recommendation = {}; // Dummy data, replace with actual recommendation logic

    res.send({
        book_name: bookName,
        recommendation: recommendation
    });
};
