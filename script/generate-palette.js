const fs = require('fs');
const path = require('path');
const { flavors } = require('@catppuccin/palette');

// Ensure the src directory exists
const targetDir = path.join(__dirname, '../src');
if (!fs.existsSync(targetDir)){
    fs.mkdirSync(targetDir);
}

// Format the object cleanly
const outputData = {};
Object.entries(flavors).forEach(([flavorName, flavorObj]) => {
  outputData[flavorName] = {};
  Object.entries(flavorObj.colors).forEach(([colorName, colorMeta]) => {
    outputData[flavorName][colorName] = {
      hex: colorMeta.hex,
      rgb: [colorMeta.rgb.r, colorMeta.rgb.g, colorMeta.rgb.b]
    };
  });
});

// Save to src/palette.json
fs.writeFileSync(
  path.join(targetDir, 'palette.json'), 
  JSON.stringify(outputData, null, 2)
);

console.log('Successfully saved palette to src/palette.json!');
