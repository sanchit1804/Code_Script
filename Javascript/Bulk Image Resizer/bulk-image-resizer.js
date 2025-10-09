const express = require('express');
const multer = require('multer');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static('public'));

const upload = multer({dest:'input/'});

app.post('/resize', upload.array('images'), async (req, res)=>{
  const height = parseInt(req.body.height);
  const width = parseInt(req.body.width);
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.tiff'];

  if(!width||!height){
    return res.status(400).send('Invalid dimensions');
  }

  if(!fs.existsSync('output')){
    fs.mkdirSync('output');
  }

  const resizedFiles = [];

  for (const file of req.files){
    const ext = path.extname(file.originalname).toLowerCase();
    if(!allowedExtensions.includes(ext)){
        console.log(`Skipped Unsupported File ${file.originalname}`);
        continue;
    }
    else{
        const outputPath = path.join('output', file.originalname);
        await sharp(file.path).resize(width, height).toFile(outputPath);
        resizedFiles.push(outputPath);
    }
  }

  res.send(`<h1>Resized ${resizedFiles.length} image(s)</h1><a href="/">Resize more</a>`);
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});