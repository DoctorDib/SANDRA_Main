
const express = require('express')
const app = express()
const port = 3000

app.use(express.static('website'));

app.get('/', (req, res) => res.sendFile("index.html", { root: './website'}));

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));
