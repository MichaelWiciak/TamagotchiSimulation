from enum import Enum
import tkinter
from tkinter import messagebox
import time
import random
import math

class CurrentState(Enum):
	
	'''This enumeration allows representing the current state of a tamagotchi
	It is used to pass the information between the window object and the pet object'''
	
	NORMAL = 0
	
	BORED = 1
	HAPPY = 2
	
	HUNGRY = 3
	FULL = 4
	
	TIRED = 5
	WIDEAWAKE = 6
	
	DEAD = 7
	
class Animation(Enum):
	
	'''This enumeration represents the current animation being played by the window object'''
	
	NONE = 0
	
	FEED = 1
	PLAY = 2
	SLEEP = 3
	WAKE = 4
	
	def Frame_Dictionary():
		return {Animation.NONE:0, Animation.FEED:2, Animation.PLAY:6, Animation.SLEEP:0, Animation.WAKE:0}
		
class Hats(Enum):
	
	'''This enumeration represents hat type'''
	
	NONE = 0
	BABYHAT = 1
	STRAWHAT = 2
	HARDHAT = 3
	COWBOY = 4
	TOPHAT = 5
	
	
class AppWindow( tkinter.Tk ):
	'''Acts as the window and runs the app'''
	
	#defines the object variables
	#window style
	Size = '450x350'
	Background_Colour = '#4fa5db'
	Secondary_Background = '#9ef0ff'
	Text_Colour = 'black'
	Font = 'Courier New'
	Font_Size = 10
	
	#game options
	Update_Interval = 600000 #10 minutes
	Animation_Frame_Rate = 500 #1 second
	
	def __init__(self):
		'''initialises the app'''
		super().__init__()
		
		#configures the window
		self.title('Tamagotchi')
		self.geometry(AppWindow.Size)
		self.configure(background = AppWindow.Background_Colour)
		self.resizable(False, False)
		
		#defines the close window protocol
		self.protocol('WM_DELETE_WINDOW', self.__closeWindow)
		
		#creates the pet
		self._pet = Pet()
		self._isDead = False
		self._isAsleep = False
		
		#we are not playing an animation
		self._currentAnimation = Animation.NONE
		self._animationFrame = 0
		
		#sets up the widgets
		#name label
		self._nameLabel = tkinter.Label(self, width=5, text="Name", font =(AppWindow.Font,AppWindow.Font_Size), fg=AppWindow.Text_Colour, bg = AppWindow.Secondary_Background)
		self._nameLabel.place(x=10, y=10)
		
		#name entry box
		self._nameVar = tkinter.StringVar(self, value = self._pet.getName())
		self._nameEntryBox = tkinter.Entry(self, textvariable = self._nameVar, font =(AppWindow.Font,AppWindow.Font_Size), fg=AppWindow.Text_Colour)
		self._nameEntryBox.place(x=55, y=10)
		
		#pet image
		self._petImageBox = tkinter.Canvas(self, width = 300, height = 300)
		self._petImageBox.place(x=20, y=40)
		self._petImage = tkinter.PhotoImage(file="Images\\NORMAL.ppm")
		self._petImageBox.create_image(150, 150,image = self._petImage)
		self._hatImage = tkinter.PhotoImage(file="Images\\NONE.ppm")
		self._hat = self._petImageBox.create_image(150,20,image = self._hatImage)
		
		#feed button
		self._feedImage = tkinter.PhotoImage(file="Images\\feedButton.ppm")
		self._feedButton = tkinter.Button(self, width = 75, height = 50, image=self._feedImage, command = self.__feed, bg = AppWindow.Secondary_Background, activebackground = AppWindow.Secondary_Background)
		self._feedButton.place(x=340, y=70)
		
		#sleep button
		self._sleepImage = tkinter.PhotoImage(file="Images\\sleepButton.ppm")
		self._sleepButton = tkinter.Button(self, width = 75, height = 50, image=self._sleepImage, command = self.__sleep, bg = AppWindow.Secondary_Background, activebackground = AppWindow.Secondary_Background)
		self._sleepButton.place(x=340, y=150)
		
		#play button
		self._playImage = tkinter.PhotoImage(file="Images\\playButton.ppm")
		self._playButton = tkinter.Button(self, width = 75, height = 50, image=self._playImage, command = self.__play, bg = AppWindow.Secondary_Background, activebackground = AppWindow.Secondary_Background)
		self._playButton.place(x=340, y=230)
		
		#performs an initial update
		self.__updateWindow()
		
		self.mainloop()
		
	def __feed(self):
		'''Feeds the pet'''
		
		#cannot eat when sleeping
		if not(self._pet.isAsleep()):
		
			#feeds the pet
			self._pet.feed()
			
			#plays the feed animation
			self._currentAnimation = Animation.FEED
			self._animationFrame = 0
			
			#stop the auto update
			self.after_cancel(self._afterRef)
			
			#start playing the animation
			self._afterRef = self.after(AppWindow.Animation_Frame_Rate, self.__playAnimation)
		
	def __sleep(self):
		'''Awakens a sleeping pet or puts to sleep a waking pet'''
		
		#stop the auto update
		self.after_cancel(self._afterRef)
		
		#start playing the animation
		self._afterRef = self.after(AppWindow.Animation_Frame_Rate, self.__playAnimation)
		
		#toggles the pet to be awake or asleep
		self._pet.toggleSleep()
		
		#determines if awake or asleep
		sleeping = self._pet.isAsleep()
		
		#if sleeping then play the put to sleep animation
		self._animationFrame = 0
		if sleeping:
			
			self._currentAnimation = Animation.SLEEP
			
		else:
			#waking up
			self._currentAnimation = Animation.WAKE
		
	def __play(self):
		'''Plays with the pet'''
		
		#cannot play when sleeping
		if not(self._pet.isAsleep()):
		
			#feeds the pet
			self._pet.play()
			
			#plays the feed animation
			self._currentAnimation = Animation.PLAY
			self._animationFrame = 0
			
			#stop the auto update
			self.after_cancel(self._afterRef)
			
			#start playing the animation
			self._afterRef = self.after(AppWindow.Animation_Frame_Rate, self.__playAnimation)
		
	def __playAnimation(self):
		'''Plays the next frame of the current animation'''
		
		#check that the animation has not finished
		if self._animationFrame < Animation.Frame_Dictionary()[self._currentAnimation]:
			
			#generate the directory of the next frame
			directory = 'Animations\\' + self._currentAnimation.name + str(self._animationFrame) + '.ppm'
			
			#set the image
			self._petImage.configure(file = directory)
			
			#increment the frame
			self._animationFrame += 1
			
			#continue the animation
			self._afterRef = self.after(AppWindow.Animation_Frame_Rate, self.__playAnimation)
			
		else:
			
			#no longer playing an animation so resume normal activity
			self._currentAnimation = Animation.NONE
			
			self._afterRef = self.after(AppWindow.Animation_Frame_Rate, self.__updateWindow)
		
	def __updateWindow(self):
		'''Updates the pet and the images on the window'''
		
		#need to update the pet every period
		self._afterRef = self.after(AppWindow.Update_Interval, self.__updateWindow)
		
		#updates the name of the pet
		self._pet.setName( self._nameVar.get() )
		
		#updates the pet
		currentState = self._pet.updateTime()
		
		#handles sleeping pet
		if self._pet.isAsleep():
			
			#handles hat movement
			if not(self._isAsleep):
				self._isAsleep = True
				
				#move the hat
				self._petImageBox.move(self._hat, 70, 80)
			
			#sets the current image
			self._petImage.configure(file = "Images\\SLEEPING.ppm")
			
		else:
			
			#handles hat movement
			if self._isAsleep:
				self._isAsleep = False
				
				#move the hat
				self._petImageBox.move(self._hat, -70, -80)
				
			#sets the current image
			self._petImage.configure(file = "Images\\"+currentState.name+".ppm")
		
		self._hatImage.configure(file = "Images\\"+self._pet.getHat().name+".ppm")
		
		#handles death
		if currentState == CurrentState.DEAD:
			
			#stop updating
			self.after_cancel(self._afterRef)
			
			self._isDead = True
			
			#lock buttons and entry box
			self._feedButton.configure(state = 'disabled')
			self._sleepButton.configure(state = 'disabled')
			self._playButton.configure(state = 'disabled')
			self._nameEntryBox.configure(state = 'disabled')
			
			#displays popup
			messagebox.showwarning("Tamagotchi", self._pet.getName()+" has died :(")
		
	def __closeWindow(self):
		'''Allows the window to close safely'''
		if not(self._isDead):
			#stops the pet update
			self.after_cancel(self._afterRef)
			#update pet manually
			self.__updateWindow()
			#stops the pet update
			self.after_cancel(self._afterRef)
		
		#destroys the window
		self.destroy()
		
		#quit the program
		quit()
		
class Pet( object ):
	'''Represents the tamagotchi itself'''
	
	MAX_FEED = 5 # upper bound for random value to feed by
	MAX_HUNGER = 100 # will obese itself to death if above this
	MAX_TIRED = 100 # possibly cannot exceed this but will not die
	MAX_JOY = 100 # possibly cannot exceed this but will not die
	MAX_PLAY = 10 # upper bound for random value to increase play by
	MAX_HAT_NUMBER = 5
	
	HUNGER_SCALE_FACTOR = 100 / (5 * 24 * 60 * 60) # the rate at which hunger increases
	
	BOREDOM_LOWER_SCALE_FACTOR = 100 /(24 * 60 * 60) # the lower range for how boredom will increase
	BOREDOM_HIGHER_SCALE_FACTOR = 1.5 * BOREDOM_LOWER_SCALE_FACTOR # the upper range for how boredom will increase
	
	TIREDNESS_SCALE_FACTOR = 100 / (48 * 60 * 60) # the rate at which tiredness increases

	SLEEP_SCALE_FACTOR = 100 / (8 * 60 * 60) # the rate at which sleep occurs
	
	HAT_AWARD_RATE = 5 * 24 * 60 * 60 # the rate (in seconds) at which hats are awarded
	
	HUNGRY_STATE = 50 # the statistic value at which the pet becomes hungry
	BORED_STATE = 50 # the statistic value at which the pet becomes bored
	TIRED_STATE = 50 # the statistic value at which the pet becomes tired
	FULL_STATE = 90 # the statistic value at which the pet becomes full
	WIDEAWAKE_STATE = 90 # the statistic value at which the pet becomes wide awake
	HAPPY_STATE = 90 # the statistic value at which the pet becomes happy
	
	DEFAULT_STATS = ["Little Niccc", 85, 85, 85, 0]

	# this is the name of the file to save and load the tamagotchi to/from
	FILE_NAME = "Data\\petData.dat"
	
	def __init__(self):
		'''Loads the tamagotchi from the file (if the file exists)
			will NOT update the pet's attributes against time automatically.
			
			If the file does not exist, then creates a new tamagotchi'''
		
		try:
			# attempt to load the tamagotchi from the file
			f = open(self.FILE_NAME, "r")
			tam = f.read()
			stats = tam.split("\n")
			
			# if the file is not empty then update the pet's attributes
			if len(stats) <= 0:
				raise Exception
			else:
				self._name = stats[0]
				self._hunger = float(stats[1])
				self._sleep = float(stats[2])
				self._play = float(stats[3])
				self._hat = int(stats[4])
				self._lastUpdate = float(stats[5])
				self._awake = stats[6] == "True"
				self._birthday = float(stats[7])
				
		except Exception as e:
			
			# file does not exist so create new tamagotchi
			self._name = self.DEFAULT_STATS[0]
			self._hunger = self.DEFAULT_STATS[1]
			self._sleep = self.DEFAULT_STATS[2]
			self._play = self.DEFAULT_STATS[3]
			self._hat = self.DEFAULT_STATS[4]
			self._lastUpdate = time.time()
			self._awake = True
			self._birthday = time.time()
		
	def setName(self, name):
		'''Updates the name of the tamagotchi
		Takes a string'''
		self._name = name
		
	def getName(self):
		'''Returns the name of the pet (string)'''
		return self._name
		
	def saveToFile(self):
		'''Saves the tamagotchi to the file'''
		
		#sets up the data frame
		data = [self._name, self._hunger, self._sleep, self._play, self._hat, self._lastUpdate, self._awake, self._birthday]
		
		file = open(self.FILE_NAME, "w")
		
		#contrusts the data string
		writeme = ""
		for x in data:
			writeme += str(x)
			writeme += "\n"
			
		file.write(writeme)
		file.close()
		
	def updateTime(self):
		'''Updates the attributes of the tamagotchi by comparing
		the last time is was updated to the current time.
		
		This will call the saveToFile method upon execution
		
		If the pet dies, then the file is deleted.
		
		This method returns a CurrentState Enumeration type'''
		
		# get current time
		currentTime = time.time()
		
		# find difference (in seconds) between last update and now
		updateDifference = currentTime - self._lastUpdate
		
		# calculate differences in qualify of life
		hungerDiff = updateDifference * self.HUNGER_SCALE_FACTOR
		joyDiff = updateDifference * random.uniform(self.BOREDOM_LOWER_SCALE_FACTOR, self.BOREDOM_HIGHER_SCALE_FACTOR)
		
		# action differences
		# no additional checks required when decrementing hunger as the pet will die due to starvation
		self._hunger -= hungerDiff

		self._play -= joyDiff

		# check to ensure joy never falls below zero - negative joy not allowed
		if self._play < 0:
			self._play = 0

		# if asleep...
		if self.isAsleep():
			# add sleep
			self._sleep += self.SLEEP_SCALE_FACTOR * updateDifference

			# if the sleep now exceeds 100, set sleep to 100 and waken the pet
			if self._sleep >= 100:
				self._sleep = 100
				self.toggleSleep()
		else:
			# otherwise if not asleep, the pet becomes more tired
			tirednessDiff = updateDifference * self.TIREDNESS_SCALE_FACTOR
			self._sleep -= tirednessDiff
		
		# determine if the tamagotchi is dead
		if self._isDead():
			self._deleteFile()
			return CurrentState.DEAD
		
		# calculate difference in seconds between birth and now
		lifespan = currentTime - self._birthday 
		
		# award hat as appropriate
		self._hat = math.floor(lifespan / self.HAT_AWARD_RATE)
 
		# update the time that the pet was last updated
		self._lastUpdate = currentTime
		
		# save the pet
		self.saveToFile()
		
		return self._determineState()
		
	def getHat(self):
		'''Returns an Hats enum corresponding the pet's current hat'''
		return Hats(min(self._hat, self.MAX_HAT_NUMBER))
		
	def isAsleep(self):
		'''Returns a bool indicating whether the pet is asleep (True) or awake (False)'''
		return not(self._awake)
		
	def feed(self):
		'''This method represents feeding the tamagotchi
		Time is not updated when this method is called'''
		food = random.uniform(0, (self.MAX_FEED))
		self._hunger += food
		
	def toggleSleep(self):
		'''This method will toggle whether the pet is sleeping or not
		Time is not updated when this method is called'''
		self._awake = not(self._awake)
		
	def play(self):
		'''This method represents playing with the tamagotchi
		Time is not updated when this method is called'''
		
		fun = random.uniform(0, self.MAX_PLAY)
		
		self._play += fun
		if self._play >= 100:
			self._play = 100
			
	def _determineState(self):
		'''This method contains the logic determining the state of the 
		pet and will return CurrentState Enumeration type'''
		
		# logic for the HUNGRY and FULL states, which takes top precedent
		if self._hunger <= self.HUNGRY_STATE:
			return CurrentState.HUNGRY
		elif self._hunger >= self.FULL_STATE:
			return CurrentState.FULL
			
		# logic for the TIRED and WIDEAWAKE states
		if self._sleep <= self.TIRED_STATE:
			return CurrentState.TIRED
		elif self._sleep >= self.WIDEAWAKE_STATE:
			return CurrentState.WIDEAWAKE
			
		# logic for the BORED and HAPPY states
		if self._play <= self.BORED_STATE:
			return CurrentState.BORED
		elif self._play >= self.HAPPY_STATE:
			return CurrentState.HAPPY
			
		# catch all case - it will be normal if none of the above conditions are met
		return CurrentState.NORMAL
		
	def _deleteFile(self):
		'''Clears the contents of the pet data file'''
		file = open(self.FILE_NAME, "w")
		file.write("")
		file.close()
		
	def _isDead(self):
		'''Determines whether the pet is dead'''
		# return True if dead
		if self._hunger <= 0:
			# died from starvation
			return True
		elif self._hunger > self.MAX_HUNGER:
			# died from obesity
			return True
		elif self._sleep <= 0:
			# died from exhaustion
			return True
		return False
		
a = AppWindow()
		
