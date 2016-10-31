#!/usr/bin/env python
# encoding: utf-8

from psychopy import core, visual, prefs, event
from baseDefsPsychoPy import *
from stimPresPsychoPy import *
from useful_functions import loadFiles #this overrides the loadFiles in baseDefs
import generateTrials

# open Google survey at the end of the experiment
import webbrowser as web

class Exp:
    def __init__(self):
        self.expName = 'LSS'
        self.surveyURL = "https://docs.google.com/forms/d/e/1FAIpQLSdAUsq7IdPQ2n2y_Gyv0xMI0bKKaHz66jrqo8ckGv3ATwP47Q/viewform?entry.214853107={subjCode}&entry.497668873={room}"
        self.path = os.getcwd()
        self.subjInfo = {
                '1':  { 'name' : 'subjCode',
                        'prompt' : 'EXP_XXX',
                        'options': 'any',
                        'default':self.expName+'_101'},
                '2':  { 'name' : 'seed',
                        'prompt' : 'Seed: ',
                        'options': 'any',
                        'default': 101},
                '3':  { 'name' : 'cuePicMapping',
                        'prompt' : 'fixed / reversed / random',
                        'options' : ('fixed', 'reversed', 'random'),
                        'default' : 'random'},
                '4' : { 'name' : 'responseDevice',
                        'prompt' : 'keyboard / gamepad',
                        'options' : ("keyboard","gamepad"),
                        'default':'keyboard'},
                '5' : { 'name' : 'data',
                        'prompt' : 'subject / practice',
                        'options' : ("subject","practice"),
                        'default':'subject'},
                '6' : { 'name' : 'room',
                        'prompt' : 'Kramer / George / Elaine / Jerry',
                        'options' : ("Kramer","George","Elaine","Jerry"),
                        'default' : 'Kramer'},
                '7' : { 'name' : 'initials',
                        'prompt' : 'experimenter initials',
                        'options' : 'any',
                        'default' : ''}
                }

        optionsReceived = False
        fileOpened = False
        while not fileOpened:
            [optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
            if not optionsReceived:
                popupError(self.subjVariables)
            elif self.subjVariables['data'] == 'practice':
                fileOpened = True
                self.subjVariables['subjCode'] = 'testing'
                self.outputFile = open('sample_data.txt','w')
            elif not os.path.isfile('data/'+self.subjVariables['subjCode']+'.txt'):
                fileOpened = True
                self.outputFile = open('data/'+self.subjVariables['subjCode']+'.txt','w')
            else:
                fileOpened = False
                popupError('That subject code already exists!')

        if self.subjVariables['responseDevice'] == 'gamepad':
            try:
                self.stick = initGamepad()
                pygame.init()
                print "Using gamepad..."
                self.inputDevice = "gamepad"
                self.validResponses = {'left':6,'right':7}  # big shoulder buttons
                responseInfo = "Press the Left big shoulder button for LEFT and the Right big shoulder button for RIGHT."
                breakInfo = "Press the Green button to continue."
            except SystemExit:
                print "No gamepad found; using keyboard..."
                self.subjVariables['responseDevice'] = 'keyboard'
                self.inputDevice = 'keyboard'
                self.validResponses = {'left':'z','right':'slash'}
                responseInfo = " Press the 'z' key for LEFT and the '/' key for 'RIGHT'."
                breakInfo = "Press any key to continue."
        else:
            print "Using keyboard..."
            self.inputDevice = 'keyboard'
            self.validResponses = {'left':'z','right':'slash'}
            responseInfo = " Press the 'z' key for LEFT and the '/' key for 'RIGHT'."
            breakInfo = "Press any key to continue."

        self.win = visual.Window(fullscr=True, color=[.6,.6,.6], allowGUI=False,
                                 monitor='testMonitor', units='pix', winType='pyglet')

        # populate survey URL with subject code and experiment room
        self.surveyURL += '&entry_0='+self.subjVariables['subjCode']+'&entry_1='+self.subjVariables['room']
        #web.open(self.surveyURL)
        self.preFixationDelay = 1.25
        self.postFixationDelay = 0.5

        self.stimPositions = {'center':(0,0), 'left':(-500,0), 'right':(500,0)}
        self.numPracticeTrials = 8
        self.takeBreakEveryXTrials = 100

        self.instructions = \
"""
Thank you for participating!

In this experiment, you will hear various words like 'dog' and 'guitar' followed by pictures appearing on the left or right side of the screen. Sometimes the words will match the pictures and sometimes they won't. All you need to do is decide as quickly as possible if the picture appears on the left or the right side of the screen.

Please answer as quickly and accurately as you can. If you make a mistake, you will hear a buzzing sound. Please let the experimenter know when you have completed reading these instructions.

"""
        self.instructions+=breakInfo

        self.takeBreak = "Please take a short break.\n\n" + breakInfo
        self.practiceTrials = "The first few trials are practice.\n\n" + breakInfo
        self.realTrials = "Now you will start the real trials! Remember to respond as quickly and accurately as you can.\n\n" + breakInfo
        self.finalText = \
"""
You've come to the end of the experiment!

A short survey should appear on the screen after you exit this screen. The first two questions of the survey should be filled in. If the survey does not appear on your screen, or the first two answers are not already filled in, please alert the experimenter. Thank you for participating!

""" + breakInfo

class ExpPresentation(Exp):
    def __init__(self,experiment):
        self.experiment = experiment

    def initializeExperiment(self):
        self.expTimer = core.Clock()
        showText(self.experiment.win, "Loading files...", color="black", waitForKey=False)
        if self.experiment.subjVariables['data'] == 'practice':
            trialsPath = 'sample_trials.csv'
        else:
            trialsPath = 'trials/seed%s.csv' % (self.experiment.subjVariables['seed'])
        if not os.path.isfile(trialsPath):
            print 'Trials file not found. Creating...'
            generateTrials.write(
                path=trialsPath,
                seed=self.experiment.subjVariables['seed'],
                cuePicMapping=self.experiment.subjVariables['cuePicMapping'],
            )
        self.pictureMatrix = loadFiles('stimuli/pictures', 'jpg', 'image', self.experiment.win)
        self.soundMatrix = loadFiles('stimuli/sounds', 'wav', 'sound', win=self.experiment.win)

        (self.trialListMatrix, self.fieldNames) = importTrials(trialsPath, method="sequential")
        self.fixSpot = visual.TextStim(self.experiment.win,text="+",height = 50,color="black")
        #self.rectOuter = newRect(self.experiment.win,size=(310,305),pos=self.experiment.stimPositions['center'],color=(.5,.5,.5))
        #self.rectInner = newRect(self.experiment.win,size=(305,305),pos=self.experiment.stimPositions['center'],color=(1,1,1))
        #self.frames = [self.rectOuter, self.rectInner]


    def checkExit(self):
        if event.getKeys() == ['equal','equal']:
            sys.exit("Exiting experiment...")

    def giveFeedback(self,isRight):
        if isRight == 1:
            #feedback = self.pictureMatrix['feedback_correct']['stim']
            print "Before", self.expTimer.getTime()
            #self.soundMatrix['bleep']['stim'].play()

            print "After", self.expTimer.getTime()
        else:
            #feedback = self.pictureMatrix['feedback_incorrect']['stim']
            self.soundMatrix['buzz']['stim'].play()

        #feedback.setPos(self.experiment.stimPositions['center'])
        #setAndPresentStimulus(self.experiment.win, [self.curPic] + [feedback])
        #core.wait(self.experiment.feedbackDelay)
        #setAndPresentStimulus(self.experiment.win, self.curPic)

    def presentTestTrial(self, whichPart, curTrial, curTrialIndex):
        self.checkExit()
        core.wait(self.experiment.preFixationDelay)
        setAndPresentStimulus(self.experiment.win, self.fixSpot) #show fixation cross
        core.wait(self.experiment.postFixationDelay)
        self.curPic = self.pictureMatrix[curTrial['pic_file']]['stim']
        self.curPic.setPos(self.experiment.stimPositions[curTrial['side']])

        #self.experiment.win.flip()
        self.soundMatrix[curTrial['cue_file']]['stim'].play()
        core.wait(self.soundMatrix[curTrial['cue_file']]['stim'].duration) #wait until the sound stops playing
        core.wait(float(curTrial['soa']))
        print 'waiting for ',curTrial['soa']
        setAndPresentStimulus(self.experiment.win,[self.fixSpot,self.curPic])

        correctResp = self.experiment.validResponses[str(curTrial['side'])]
        if self.experiment.inputDevice == 'keyboard':
            (response,rt) = getKeyboardResponse(self.experiment.validResponses.values())
        elif self.experiment.inputDevice == 'gamepad':
            (response,rt) = getGamepadResponse(self.experiment.stick,self.experiment.validResponses.values())

        isRight = 0
        if response == correctResp:
            isRight = 1
        self.giveFeedback(isRight)
        self.experiment.win.flip()

        fieldVars=[]
        for curField in self.fieldNames:
            fieldVars.append(curTrial[curField])
        [header, curLine] = createRespNew(self.experiment.subjInfo, self.experiment.subjVariables, self.fieldNames, fieldVars,
                                        a_whichPart = whichPart,
                                        b_curTrialIndex = curTrialIndex,
                                        c_expTimer = self.expTimer.getTime(),
                                        d_isRight = isRight,
                                        e_rt = rt*1000)
        writeToFile(self.experiment.outputFile,curLine)

        if curTrialIndex==0 and not whichPart=='practice':
            print "Writing header to file..."
            dirtyHack = {}
            dirtyHack['trialNum']=1
            writeHeader(dirtyHack, header,'header_'+self.experiment.expName)

    def cycleThroughExperimentTrials(self,whichPart):
        curTrialIndex = 0
        if whichPart == "practice":
            trialIndices = random.sample(range(1,50), self.experiment.numPracticeTrials)
            for curPracticeTrial in trialIndices:
                self.presentTestTrial(whichPart,
                         self.trialListMatrix.getFutureTrial(curPracticeTrial),
                         curTrialIndex)
        else:
            curBlock = 0
            for curTrial in self.trialListMatrix:
                if curTrial['block'] > curBlock:
                    showText(self.experiment.win, self.experiment.takeBreak, color=(1,1,1), inputDevice=self.experiment.inputDevice) #take a break
                    curBlock += 1
                self.presentTestTrial(whichPart, curTrial, curTrialIndex)
                curTrialIndex += 1
            self.experiment.outputFile.close()

currentExp = Exp()
currentPresentation = ExpPresentation(currentExp)
currentPresentation.initializeExperiment()
showText(currentExp.win,currentExp.instructions,color=(-1,-1,-1),inputDevice=currentExp.inputDevice) #show the instructions for test
showText(currentExp.win,currentExp.practiceTrials,color=(-1,-1,-1),inputDevice=currentExp.inputDevice)
currentPresentation.cycleThroughExperimentTrials("practice")
showText(currentExp.win,currentExp.realTrials,color=(-1,-1,-1),inputDevice=currentExp.inputDevice)
currentPresentation.cycleThroughExperimentTrials("test")
showText(currentExp.win,currentExp.finalText,color=(-1,-1,-1),inputDevice=currentExp.inputDevice) #thank the subject
web.open(currentExp.surveyURL.format(**currentExp.subjVariables))
