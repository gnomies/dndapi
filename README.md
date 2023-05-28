# dndapi

This app creates a dnd character with a name a class a race and one piece of equipment. Then uses ChatGPT to create a backstory. The cost per NPC creation is around USD$0.01 using text-davinci-003. This is my first time working with APIs so things may get strange. Happy NPC making.

Current Features
Running python creator.py will call [on dnd](https://www.dnd5eapi.co) and request a random race, class, and equipment. Then it will use chatGPT with the prompt "Generate a unique name for a fantasy character" with a max call of 30 tokens (Fantasy names can be strange y'all)

Then create a back story based on created characters Name Race and Equipment. 

ChatGPT Token Breakdown
text-davinci, 2 requests - 29 prompt + 295 completion = 324 tokens
text-davinci, 2 requests - 31 prompt + 329 completion = 360 tokens

Character Example 1
Character Name Erinthra Malkaine
Race: human, 
Class: barbarian
Equipment: horse-riding-battle-axe
Backstory:

Her family had been riding and taming horses for generations, so Erinthra was born into a legacy of horsemanship.

At the age of 17, Erinthra ventured out alone to explore the wider world. She made her way to a large city, where she heard tales of far away lands and grand battles. Inspired by these stories, she decided to join 
up with a mercenary group to travel abroad and seek her fortune.

For the next few years, Erinthra traveled extensively, taking part in grueling campaigns and fighting as a frontline warrior in numerous battles. Through these experiences she developed great strength and acumen, and soon became known for her prowess in combat.

On her travels, Erinthra found an old, rusty horse-riding battle axe. She brought it back to her home village and restored it to its former glory, using skills she had developed from working with her family’s horses. From then on, Erinthra carried this trusty weapon with her wherever she went, and it became a symbol of her strength and prowess.

Now, Erinthra has returned to her home village as a wise and experienced warrior. She still rides and tames horses with her family, and continues to carry her battle axe into battle, striking fear into the hearts of her enemies.

Character Example 2
Character Name: Adelina Silverstar
Race: human
Class: bard
Equipment: censer

Backstory:
Adelina Silverstar was born to a small family of travelling merchants in a far away medieval kingdom. Her parents were quite successful in their trade and Adelina was able to receive a good education, and even learn a few choice magical arts. Adelina had quite a fondness for singing and often sang stories of courage and heroism while playing her lute.

One day her travels took her to a temple dedicated to the gods of music and enlightenment. There she found a sacred censer atop a pedestal, curiously crafted in the shape of a soaring star. Without thinking, Adelina reached for it and suddenly the censer glowed brightly, calling upon Adeline as its beholder. The guardian of the temple quickly noticed Adelina's affinity with the sacred item and tasked Adelina with the job of playing beautiful music throughout the kingdom and promoting peace amongst the warring factions.

Adelina accepted the task and with her newfound magical powers, learned how to play even more intricate and beautiful songs. Travelling throughout the kingdom, Adelina was able to bring peace through her singing and the magical power of the censer. She was known as the Silverstar Bard and was respected and admired by all.

Adelina now carries the power of the censer wherever she goes, illuminating and warming the hearts of all those she meets with her beautiful tunes and inspiring stories.


Near Future plans:
  - Web interface using Flask/Flet/FastAPI 
  - Searchable Database for past characters.
  - Text Fields for City Country Job
  - Character Stat rolling for base stats 4d6 drop lowest
  - implement character name request based on race and possibly class.
Far Future Plans
  - Dall-e intigration to create a quick and dirty portrait. (estimated to cost around $0.04 per character) 
  - Export to Obsidian Templiter Markdown for Character sheets and use in obsidian for campaign management
  - 
