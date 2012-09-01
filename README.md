bomb_seek
=========

A Simple distributed AI app - map text file : * = wall, {0-9} = agents, A = Scout 
- handle from 1 to 10 agents										
- Gui															
- Select and Deselect agent with buttons and show their path
- Agents should exchange paths and knowledge			
- Start, Stop, Restart functionality 				
- Dump some Statistics to a file

Description:
============
Agents start seeking for the Bomb
- if an agent finds the bomb:
	- starts seeking the Scout to inform him about the bomb
	- if the Scout finds where the bomb is he should go to deactivate it.
- if an agend finds another one
	- they exchange information about the known path and the location of the bomb
