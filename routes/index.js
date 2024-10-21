const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const recommendController = require('../controllers/recommendController');

// Define routes
router.get('/', homeController.home);
router.post('/recommend', recommendController.recommend);

module.exports = router;
