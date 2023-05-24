# ![Icon](Icons/icon.png)TPadder

TPadder is a simple application that allows you to turn an item texture into an tile texture.

Terraria requires mutliblock tiles to have a 2 pixel padding between each block (a block is 16x16 pixels). Since doing this manually can become increasingly tedious for larger scale mods, I've made a simple application to take a non-padded texture and convert it into a padded tile texture. Additionally, it can also generate a highlight texture for any tile that interacts with the smart cursor in game.

### Example

![Example](Example/Example.png)

### Note

For the best outcome, ensure that the source texture has dimensions that are multiples of 16px. Deviation from this guideline may result in unexpected results.

If your texture does is not have the correct dimensions, change your texture's canvas size to the correct dimensions and center your texture.

For optimal results, it is important to ensure that the source texture has dimensions that are multiples of 16px. Deviating from this guideline may result in unexpected results.

if your texture does not have the correct dimensions, follow these steps to adjust it:

1. Change the canvas size of your texture to match the correct dimensions by adding or removing pixels as necessary.
2. Center your texture within the adjusted canvas.


### Contribution

Contributions, forks, and feedback are all welcome! Feel free to contribute to TPadder's development, suggest improvements or report any issues on the GitHub repository.

### License

TPadder is released under the GNU General Public License v3, allowing you to freely use, modify, and distribute the mod in accordance with the terms outlined in the license.
