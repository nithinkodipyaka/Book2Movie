const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to serve static files
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Set up routes
app.use('/', require('./routes/index'));

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
