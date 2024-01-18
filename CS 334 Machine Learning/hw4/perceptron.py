import argparse
import numpy as np
import pandas as pd
import time

class Perceptron(object):
    mEpoch = 1000  # maximum epoch size
    w = None       # weights of the perceptron (1-d array)

    def __init__(self, epoch):
        self.mEpoch = epoch

    def train(self, xFeat, y):
        """
        Train the perceptron using the data

        Parameters
        ----------
        xFeat : nd-array with shape n x d
            Training data 
        y : 1d array with shape n
            Array of responses associated with training data.

        Returns
        -------
        stats : object
            Keys represent the epochs and values the number of mistakes
        """
        stats = {}
        self.w = np.random.rand(xFeat.shape[1])

        for e in range(1, self.mEpoch+1):
            p = np.random.permutation(len(xFeat))
            data_x = xFeat[p]
            data_y = y[p]
            m = 0
            for row in range(len(data_x)):
                su = self.sample_update(data_x[row], data_y[row])
                self.w = su[0]
                m += su[1]
                
            stats.update({e:m})
            
            if m == 0:
                break

        return stats

    def sample_update(self, xi, y):
        """
        Given a single sample, give the resulting update to the weights

        Parameters
        ----------
        xi : numpy array of shape 1 x d
            Training sample 
        y : single value (-1, +1)
            Training label

        Returns
        -------
            wnew: numpy 1d array
                Updated weight value
            mistake: 0/1 
                Was there a mistake made 
        """
        yHat = np.sign(np.dot(xi, self.w))
        yHat = 1 if yHat >= 0 else -1
        mistake = int(y - yHat)
        if mistake == 0:
            wnew = self.w
        if mistake > 0:
            wnew = self.w + xi
        if mistake < 0:
            wnew = self.w - xi
        return wnew, 0 if mistake == 0 else 1

    def predict(self, xFeat):
        """
        Given the feature set xFeat, predict 
        what class the values will have.

        Parameters
        ----------
        xFeat : nd-array with shape m x d
            The data to predict.  

        Returns
        -------
        yHat : 1d array or list with shape m
            Predicted response per sample
        """
        yHat = []
        yHat = np.sign(np.dot(xFeat, self.w))
        yHat = [1 if x>= 0 else -1 for x in yHat]

        return yHat


def transform_y(y):
    """
    Given a numpy 1D array with 0 and 1, transform the y 
    label to be -1 and 1

    Parameters
    ----------
    y : numpy 1-d array with labels of 0 and 1
        The true label.      

    Returns
    -------
    y : numpy 1-d array with labels of -1 and 1
        The true label but 0->1 
    """
    for i in range(len(y)):
        y[i] = int(y[i] == 1) - int(y[i] == 0) 
    return y

def calc_mistakes(yHat, yTrue):
    """
    Calculate the number of mistakes
    that the algorithm makes based on the prediction.

    Parameters
    ----------
    yHat : 1-d array or list with shape n
        The predicted label.
    yTrue : 1-d array or list with shape n
        The true label.      

    Returns
    -------
    err : int
        The number of mistakes that are made
    """
    err = 0
    for i in range(len(yHat)):
        err += (1*(yHat[i] != yTrue[i]))

    return err


def file_to_numpy(filename):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    return df.to_numpy()



def tune_perceptron(trainx, trainy, epochList):
    """
    Tune the preceptron to find the optimal number of epochs

    Parameters
    ----------
    trainx : a nxd numpy array
        The input from either binary / count matrix
    trainy : numpy 1d array of shape n
        The true label.    
    epochList: a list of positive integers
        The epoch list to search over  

    Returns
    -------
    epoch : int
        The optimal number of epochs
    """
    x, y = trainx, trainy
    k = 3
    batch = int(len(x)/5)
    p = np.random.permutation(len(x))
    x, y = x[p], y[p]

    for e in epochList:
        s = time.time()
        mistakes = 100000
        m = Perceptron(e)
        batch_mistakes = 0
        for i in range(k):
            sub_x = x[k*batch: batch*(k+1)]
            sub_y = y[k*batch: batch*(k+1)]
            stats = m.train(sub_x, sub_y)
            batch_mistakes += calc_mistakes(m.predict(sub_x), sub_y)
            # print(batch_mistakes)
        mis = batch_mistakes/batch
        end = time.time()-s
        # print("Tuning: ",mis)
        if mis < mistakes:
            mistakes = mis
            epoch = e
        if mis == 0:
            return e
        if end > 480:
            return epoch
    return epoch


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("xTrain",
                        help="filename for features of the training data")
    parser.add_argument("yTrain",
                        help="filename for labels associated with training data")
    parser.add_argument("xTest",
                        help="filename for features of the test data")
    parser.add_argument("yTest",
                        help="filename for labels associated with the test data")
    parser.add_argument("epoch", type=int, help="max number of epochs")
    parser.add_argument("--seed", default=334, 
                        type=int, help="default seed number")
    
    args = parser.parse_args()
    # load the train and test data assumes you'll use numpy
    xTrain = file_to_numpy(args.xTrain)
    yTrain = file_to_numpy(args.yTrain)
    xTest = file_to_numpy(args.xTest)
    yTest = file_to_numpy(args.yTest)
    # transform to -1 and 1
    yTrain = transform_y(yTrain)
    yTest = transform_y(yTest)

    b1 = np.ones((xTrain.shape[0], 1))
    b2 = np.ones((xTest.shape[0], 1))
    xTrain = np.hstack((b1, xTrain))
    xTest = np.hstack((b2, xTest))

    np.random.seed(args.seed)   
    model = Perceptron(args.epoch)
    trainStats = model.train(xTrain, yTrain)
    print(trainStats)
    yHat = model.predict(xTest)
    yHat_train = model.predict(xTrain)
    # print out the number of mistakes
    test_mis = calc_mistakes(yHat, yTest)
    train_mis = calc_mistakes(yHat_train, yTrain)
    print("Number of mistakes on the test dataset", test_mis)
    print("Number of mistakes on the test dataset", test_mis/len(xTest))
    print("Number of mistakes on the test dataset for Training", train_mis)
    print("Number of mistakes on the test dataset for Training", train_mis/len(xTrain))
    print(tune_perceptron(xTrain, yTrain, [10, 50, 100, 200]))

    ## For 2D
    original_list = ['again', 'redhat', 'north', 'lcd', 'son', 'movi', 'tast', 'et', 'intellectu', 'presum', 'someth', 'otherwis', 'star', 'evolv', 'michael', 'separ', 'merchant', 'lawsuit', 'rom', 'congratul', 'in', 'patch', 'alert', 'process', 'pocket', 'flag', 'funni', 'backup', 'premium', 'acquir', 'resum', 'march', 'quot', 'break', 'factor', 'featur', 'carefulli', 'un', 'confer', 'where', 'fals', 'fill', 'ow', 'collect', 'cent', 'step', 'dure', 'monei', 'life', 'restrict', 'ban', 'video', 'python', 'happen', 'cite', 'old', 'so', 'special', 'histori', 'confid', 'usag', 'colleg', 'realiz', 'length', 'harlei', 'sometim', 'near', 'perform', 'road', 'ar', 'jim', 'remind', 'tmp', 'experienc', 'run', 'neighbor', 'specifi', 'dvd', 'summer', 'ag', 'mous', 'nearli', 'hook', 'other', 'lose', 'steal', 'binari', 'dir', 'distributor', 'ian', 'young', 'blame', 'entertain', 'overlook', 'chri', 'competit', 'against', 'london', 'weight', 'microsoft', 'stuff', 'juli', 'onli', 'joseph', 'about', 'ethic', 'enter', 'individu', 'third', 'accept', 'share', 'real', 'led', 'agreeabl', 'volum', 'ratio', 'got', 'ibm', 'ben', 'tool', 'hesit', 'wasn', 'jul', 'station', 'britain', 'h', 'understand', 'main', 'agent', 'gone', 'convert', 'broken', 'emerg', 'notic', 'detail', 'fashion', 'how', 'sh', 'put', 'suppos', 'numbernd', 'leav', 'ground', 'indian', 'path', 'bonu', 'quit', 'languag', 'broad', 'sophist', 'pro', 'probabl', 'earn', 'chang', 'softwar', 'do', 'aug', 'hello', 'rapidli', 'syntax', 'anyon', 'subject', 'correct', 's', 'format', 'valhalla', 'arrang', 'vice', 'zoom', 'circumst', 'copi', 'america', 'inconveni', 'organ', 'everyth', 'gather', 'overal', 'world', 'repli', 'numberst', 'purchas', 'vote', 'fridai', 'gibbon', 'go', 'arriv', 'air', 'role', 'none', 'er', 'd', 'hope', 'vendor', 'sourc', 'assist', 'profil', 'tremend', 'thought', 'easiest', 'account', 'password', 'review', 'recal', 'toward', 'cost', 'twice', 'want', 'tweak', 'solv', 'still', 'scale', 'filenam', 'ident', 'alreadi', 'conduct', 'chines', 'side', 'someon', 'charact', 'pound', 'monthli', 'evalu', 'fix', 'therefor', 'assur', 'evolut', 'new', 'c', 'fiction', 'iii', 'weekend', 'sort', 'inlin', 'speed', 'essenti', 'bandwidth', 'invest', 'health', 'report', 'upon', 'creat', 'incorpor', 'extract', 'without', 'match', 'map', 'branch', 'which', 'sell', 'retir', 'center', 'differ', 'impact', 'search', 'allow', 'rpm', 'translat', 'could', 'hmm', 'code', 'abil', 'oper', 'cross', 'decent', 'polit', 'skip', 'disk', 'outsid', 'quick', 'close', 'local', 'level', 'suit', 'enterpris', 'reserv', 'and', 'gnome', 'hp', 'amount', 'fantasi', 'global', 'commerc', 'nort', 'adopt', 'gambl', 'limit', 'conveni', 'plugin', 'patent', 'her', 'sheet', 'option', 'numberenumb', 'db', 'numberth', 'wow', 'media', 'make', 'wors', 'down', 'header', 'damn', 'specialist', 'non', 'lack', 'protocol', 'detect', 'algorithm', 'gnu', 'drink', 'ideal', 'numbercnumb', 'respond', 'holidai', 'encourag', 'matthia', 'assum', 'coverag', 'regardless', 'request', 'might', 'receiv', 'specif', 'richard', 'exampl', 'e', 'plenti', 'anywher', 'rh', 'spread', 'sit', 'hasn', 'massiv', 'journal', 'comparison', 'interfac', 'manag', 'seven', 'load', 'been', 'complex', 'citi', 'excess', 'gave', 'robert', 'current', 'valid', 'death', 'grown', 'fault', 'tire', 'below', 'thinkgeek', 'rare', 'aggress', 'exercis', 'preserv', 'central', 'ga', 'btw', 'helvetica', 'oblig', 'chain', 'prefer', 'kernel', 'variou', 'ask', 'associ', 'aol', 'equiti', 'arial', 'believ', 'devot', 'rich', 'advantag', 'particip', 'autom', 'challeng', 'panel', 'calcul', 'name', 'mysql', 'al', 'ad', 'expir', 'pursu', 'width', 'sold', 'execut', 'rid', 'help', 'press', 'audienc', 'list', 'hat', 'domin', 'admin', 'contact', 'career', 'read', 'charg', 'hint', 'privileg', 'heart', 'printer', 'crap', 'oh', 'mid', 'committe', 'unknown', 'exist', 'rss', 'wonder', 'often', 'entri', 'mix', 'major', 'prior', 'clock', 'instruct', 'registr', 'countri', 'joke', 'recov', 'honest', 'foundat', 'maker', 'procedur', 'defend', 'winner', 'webcam', 'yield', 'extern', 'difficult', 'question', 'snumber', 'award', 'hurt', 'up', 'write', 'restor', 'settlement', 'rememb', 'send', 'defin', 'friendli', 'entrepreneur', 'render', 'wrinkl', 'resolut', 'materi', 'street', 'quarter', 'propos', 'late', 'though', 'memori', 'civil', 'get', 'concern', 'randomli', 'plan', 'virginia', 'good', 'dedic', 'percent', 'worth', 'seri', 'distro', 'debat', 'oct', 'amaz', 'dont', 'posit', 'definit', 'mainten', 'offic', 'escap', 'drunken', 'knew', 'ilug', 'deposit', 'further', 'copyright', 'chat', 'staff', 'unlimit', 'unabl', 'offici', 'girl', 'experi', 'tel', 'cheer', 'view', 'becaus', 'wednesdai', 'here', 'fastest', 'renam', 'includ', 'satisfact', 'setup', 'disabl', 'or', 'affili', 'border', 'advic', 'sign', 'month', 'senior', 'declar', 'enabl', 'ourselv', 'bright', 'ac', 'rnumber', 'slightli', 'park', 'zone', 'mr', 'relai', 'sampl', 'safe', 'middl', 'photo', 'lender', 'icq', 'ye', 'washington', 'spent', 'edward', 'circl', 'ugli', 'com', 'program', 'tabl', 'type', 'bore', 'sa', 'gotten', 'possibl', 'deathtospamdeathtospamdeathtospam', 'newspap', 'finish', 'unfortun', 'mother', 'perfectli', 'obvious', 'worst', 'secur', 'ten', 'refus', 'between', 'sir', 'implement', 'system', 'consider', 'investor', 'em', 'interact', 'noth', 'growth', 'dell', 'lowest', 'pr', 'dozen', 'victim', 'forc', 'zero', 'candid', 'server', 'through', 'score', 'elect', 'vari', 'mount', 'trend', 'possess', 'student', 'constantli', 'gnupg', 'bnumber', 'object', 'dollarnumb', 'medic', 'hous', 'modifi', 'pointer', 'democrat', 'shaw', 'yeah', 'nor', 'year', 'let', 'worri', 'r', 'front', 'browser', 'pattern', 'economi', 'learn', 'pain', 'bodi', 'bai', 'if', 'fit', 'bed', 'car', 'success', 'headlin', 'simpl', 'usual', 'brain', 'privat', 'focu', 'reveal', 'appreci', 'simpli', 'opt', 'mike', 'precis', 'forward', 'mind', 'equival', 'game', 'enhanc', 'desir', 'lock', 'rather', 'java', 'everywher', 'dnumber', 'fat', 'pure', 'difficulti', 'that', 'tip', 'too', 'reason', 'ext', 'relax', 'routin', 'same', 'll', 'ey', 'decemb', 'david', 'night', 'himself', 'revenu', 'keep', 'mozilla', 'you', 'neg', 'husband', 'behalf', 'etc', 'wouldn', 'nice', 'extend', 'cnumber', 'est', 'refund', 'thu', 'bulk', 'network', 'reach', 'electron', 'freedom', 'ma', 'user', 'china', 'attornei', 'lawrenc', 'black', 'mailer', 'becom', 'save', 'rock', 'degre', 'meant', 'scienc', 'democraci', 'cnet', 'exmh', 'gnumber', 'germani', 'throw', 'carri', 'spam', 'truli', 'throughout', 'spend', 'gain', 'known', 'proven', 'succe', 'doc', 'pretti', 'xml', 'anytim', 'writer', 'plu', 'numbermb', 'dev', 'rest', 'directli', 'numberbit', 'farm', 'yesterdai', 'record', 'strength', 'feet', 'curiou', 'trick', 'prepar', 'sf', 'numbertnumb', 'moment', 'sexual', 'creativ', 'excel', 're', 'few', 'custom', 'sure', 'pack', 'ct', 'm', 'ani', 'alsa', 'portabl', 'wide', 'drug', 'two', 'null', 'idea', 'william', 'averag', 'bar', 'contribut', 'somewhat', 'colleagu', 'suffer', 'varieti', 'decis', 'stai', 'extens', 'warm', 'hash', 'howev', 'diet', 'driver', 'thread', 'discov', 'daniel', 'valuabl', 'institut', 'depend', 'much', 'hassl', 'alter', 'popul', 'dead', 'sake', 'depart', 'austin', 'over', 'attract', 'okai', 'give', 'wise', 'numberf', 'speech', 'liber', 'natur', 'token', 'insur', 'their', 'anybodi', 'stori', 'focus', 'plant', 'wrote', 'out', 'platform', 'fl', 'boston', 'shanumb', 'bearer', 'vast', 'mess', 'thi', 'schedul', 'them', 'file', 'argu', 'bone', 'n', 'everyon', 'uk', 'plug', 'murphi', 'spain', 'broadband', 'eventu', 'carrier', 'track', 'warn', 'agreement', 'shock', 'tuesdai', 'entir', 'respons', 'avoid', 'identifi', 'speak', 'consid', 'fire', 'anoth', 'tune', 'alwai', 'fresh', 'usdollarnumb', 'descript', 'wind', 'dramat', 'highlight', 'payment', 'alan', 'mime', 'spamassassin', 'reward', 'bear', 'currenc', 'guarante', 'think', 'latest', 'pda', 'firewal', 'favor', 'larg', 'top', 'frame', 'singl', 'onc', 'imag', 'surround', 'pair', 'need', 'thing', 'roman', 'clear', 'school', 'trial', 'intent', 'wholesal', 'is', 'effort', 'insert', 'hotmail', 'kate', 'cours', 'russel', 'less', 'lead', 'le', 'numberd', 'eat', 'fell', 'never', 'white', 'perman', 'revis', 'function', 'see', 'econom', 'httpaddr', 'product', 'asset', 'check', 'myself', 'builder', 'legitim', 'crimin', 'exact', 'modern', 'context', 'everi', 'releas', 'gt', 'eugen', 'enforc', 'occur', 'basic', 'explain', 'after', 'fine', 'bought', 'cycl', 'pleasur', 'five', 'analysi', 'risk', 'develop', 'satisfi', 'empir\n', 'card', 'reject', 'default', 'mean', 'document', 'spamd', 'januari', 'lo', 'bet', 'cio', 'mon', 'ascii', 'squar', 'maxim', 'hopefulli', 'numberb', 'geek', 'found', 'all', 'font', 'certainli', 'elig', 'export', 'debian', 'faq', 'standard', 'express', 'cach', 'fact', 'firm', 'luck', 'intellig', 'corp', 'fund', 'penni', 'of', 'shell', 'california', 'solari', 'crack', 'excit', 'forget', 'signific', 'hardwar', 'zip', 'besid', 'yahoo', 'happi', 'els', 'choos', 'thei', 'album', 'requir', 'ms', 'matter', 'hit', 'live', 'lesson', 'parent', 'pudg', 'channel', 'ventur', 'sun', 'unit', 'oppos', 'sector', 'batch', 'futur', 'veri', 'access', 'proxi', 'event', 'twenti', 'su', 'valu', 'don', 'www', 'industri', 'hotel', 'sale', 'stuck', 'explan', 'situat', 'respect', 'heat', 'then', 'woman', 'b', 'a', 'both', 'ram', 'background', 'split', 'manufactur', 'impress', 'built', 'craig', 'summari', 'knowledg', 'region', 'verifi', 'even', 'until', 'mai', 'org', 'realli', 'k', 'investig', 'later', 'hear', 'pm', 'bottl', 'uniqu', 'mirror', 'pablo', 'client', 'big', 'far', 'act', 'scratch', 'bunch', 'conclud', 'corrupt', 'work', 'yet', 'biz', 'million', 'cartridg', 'inch', 'crazi', 'travel', 'am', 'numberxnumb', 'state', 'entiti', 'doubt', 'fee', 'fi', 'folk', 'qualifi', 'co', 'beat', 'seem', 'silli', 'initi', 'numberanumb', 'chanc', 'left', 'couldn', 'wife', 'damag', 'dealer', 'zdnet', 'nation', 'appeal', 'printabl', 'bigger', 'refin', 'polic', 'ireland', 'manual', 'task', 'emploi', 'us', 'film', 'web', 'net', 'googl', 'saturdai', 'end', 'presenc', 'dr', 'distanc', 'commiss', 'wait', 'solid', 'barcelona', 'effici', 'boi', 'modem', 'cat', 'foreign', 'demo', 'famou', 'but', 'paul', 'procmail', 'combin', 'purpos', 'equip', 'dn', 'nbsp', 'gpg', 'head', 'perhap', 'duncan', 'hnumber', 'properti', 'filter', 'integr', 'fri', 'permit', 'edit', 'predict', 'when', 'assign', 'west', 'canada', 'anymor', 'to', 'potenti', 'dig', 'mere', 'televis', 'ti', 'cnn', 'gari', 'lab', 'porn', 'medium', 'address', 'war', 'de', 'finger', 'great', 'lai', 'last', 'primari', 'vircio', 'improv', 'whose', 'six', 'henc', 'p', 'grab', 'compon', 'construct', 'inc', 'past', 'imho', 'lover', 'club', 'town', 'price', 'unless', 'adult', 'second', 'compet', 'kei', 'south', 'byte', 'field', 'minut', 'fundament', 'owner', 'teach', 'spot', 'invit', 'reg', 'machin', 'ebook', 'suffici', 'certifi', 'mobil', 'care', 'agenc', 'engag', 'dial', 'irish', 'stage', 'da', 'whole', 'establish', 'feel', 'regul', 'transmiss', 'erect', 'numberam', 'tend', 'isp', 'san', 'obviou', 'awar', 'mani', 'configur', 'strang', 'var', 'cancel', 'exchang', 'hole', 'comprehens', 'perlnumb', 'licens', 'qualiti', 'debt', 'troubl', 'quickli', 'franc', 'underwrit', 'convers', 'insist', 'la', 'train', 'relat', 'decid', 'written', 'congress', 'pentium', 'deliv', 'equal', 'mailbox', 'newest', 'mail', 'novemb', 'trip', 'almost', 'free', 'social', 'dai', 'music', 'outlook', 'part', 'partner', 'on', 'select', 'radio', 'stabl', 'remov', 'encrypt', 'garrigu', 'prevent', 'rah', 'men', 'wi', 'upgrad', 'truth', 'short', 'raw', 'maximum', 'visit', 'doer', 'ca', 'toi', 'england', 'visual', 'shop', 'face', 'tradit', 'saou', 'except', 'high', 'asid', 'categori', 'root', 'architectur', 'significantli', 'due', 'such', 'describ', 'refer', 'octob', 'phrase', 'fortun', 'sens', 'brent', 'blank', 'ftp', 'pop', 'anim', 'signatur', 'retail', 'loos', 'numbera', 'abus', 'caught', 'manner', 'graphic', 'least', 'went', 'concentr', 'usb', 'servic', 'traffic', 'resourc', 'vnumber', 'somehow', 'famili', 'everybodi', 'francisco', 'tell', 'l', 'titl', 'draft', 'till', 'beach', 'danger', 'belief', 'postal', 'determin', 'with', 'lt', 'art', 'classifi', 'box', 'hate', 'constitut', 'import', 'easi', 'caus', 'palm', 'than', 'round', 'expand', 'energi', 'trust', 'certain', 'union', 'comp', 'administr', 'layer', 'claim', 'easier', 'attent', 'dice', 'longer', 'announc', 'smart', 'fuel', 'faith', 'what', 'publish', 'menu', 'techniqu', 'steve', 'comput', 'cloth', 'by', 'treat', 'frustrat', 'also', 'desktop', 'adapt', 'nextpart', 'condit', 'fair', 'suggest', 'deal', 'bill', 'capit', 'first', 'id', 'sound', 'togeth', 'beberg', 'true', 'subscrib', 'rick', 'brought', 'mass', 'laptop', 'defens', 'multipl', 'sai', 'frequent', 'relev', 'complianc', 'unlik', 'buck', 'sport', 'exclus', 'usr', 'interview', 'sight', 'teledynam', 'didn', 'abl', 'session', 'canon', 'picasso\n', 'wealth', 'open', 'regist', 'common', 'mo', 've', 'research', 'unusu', 'behind', 'router', 'gift', 'weird', 'agre', 'audio', 'todai', 'via', 'paid', 'correspond', 'issn', 'resid', 'off', 'isn', 'cannot', 'lost', 'replac', 'cultur', 'western', 'class', 'smith', 'profit', 'indic', 'ng', 'try', 'distribut', 'aid', 'necessarili', 'back', 'higher', 'mastercard', 'discuss', 'mark', 'target', 'estat', 'appear', 'gold', 'recipi', 'offer', 'serious', 'direct', 'numberx', 'decor', 'mention', 'rank', 'sum', 'worker', 'billion', 'topic', 'done', 'fan', 'univers', 'roger', 'w', 'week', 'employ', 'ride', 'domain', 'processor', 'can', 'turn', 'yourself', 'societi', 'straight', 'concept', 'host', 'east', 'hewlett', 'weekli', 'afford', 'arm', 'sub', 'pre', 'digit', 'telephon', 'follow', 'resolv', 'number\n', 'beauti', 'hard', 'incred', 'hell', 'per', 'buffer', 'board', 'seriou', 'rel', 'highest', 'st', 'hang', 'imposs', 'extrem', 'superior', 'apart', 'drop', 'had', 'tape', 'reduct', 'item', 'tim', 'complic', 'slow', 'cheaper', 'poor', 'reboot', 'my', 'here\n', 'transmit', 'transact', 'present', 'numberp', 'mason', 'regard', 'water', 'compaq', 'bu', 'reserv\n', 'involv', 'john', 'hour', 'multipart', 'consum', 'father', 'geeg', 'walk', 'cabl', 'inspir', 'battl', 'buyer', 'across', 'remark', 'banner', 'i', 'advanc', 'input', 'src', 'strictli', 'brian', 'catalog', 'suck', 'capac', 'failur', 'justic', 'onto', 'crucial', 'she', 'submit', 'monitor', 'toll', 'peopl', 'whatev', 'occasion', 'jame', 'threaten', 'destroi', 'dublin', 'why', 'exactli', 'mortgag', 'startup', 'red', 'core', 'skin', 'trace', 'email', 'daili', 'launch', 'niall', 'bring', 'remain', 'settl', 'scan', 'euro', 'tue', 'config', 'now', 'opportun', 'margin', 'legal', 'each', 'the', 'urg', 'spammer', 'phone', 'surviv', 'unseen', 'independ', 'cb', 'test', 'programm', 'internet', 'tv', 'director', 'plai', 'cell', 'deni', 'wrap', 'oil', 'human', 'mnumber', 'feedback', 'fall', 'cv', 'judg', 'forev', 'interrupt', 'whom', 'msn', 'green', 'welch', 'team', 'plain', 'smaller', 'around', 'relationship', 'stand', 'signal', 'ham', 'analyst', 'solicit', 'love', 'wrong', 'fight', 'pick', 'listen', 'sponsor', 'welcom', 'govern', 'gai', 'aren', 'retain', 'handl', 'bond', 'within', 'environ', 'case', 'revok', 'captur', 'hire', 'profession', 'harm', 'membership', 'figur', 'guess', 'boost', 'revers', 'bank', 'attend', 'ah', 'befor', 'script', 'navig', 'updat', 'favorit', 'ce', 'hover', 'util', 'theori', 'appropri', 'bother', 'right', 'anywai', 'rival', 'hei', 'successfulli', 'port', 'se', 'warranti', 'medicin', 'clearli', 'credit', 'inbox', 'appl', 'sep', 'fax', 'popular', 'fed', 'europ', 'es', 'public', 'feed', 'aspect', 'declin', 'automat', 'seed', 'race', 'well', 'compil', 'ultim', 'wa', 'took', 'letter', 'ton', 'infrastructur', 'hacker', 'ne', 'vulner', 'have', 'linux', 'gui', 'razornumb', 'bug', 'y', 'php', 'print', 'hack', 'gordon', 'number', 'instead', 'spare', 'fork', 'text', 'wed', 'did', 'cooper', 'roll', 'transfer', 'enumb', 'meet', 'element', 'appli', 'thank', 'dear', 'base', 'nt', 'prioriti', 'reflect', 'freebsd', 'emailaddr\n', 'variabl', 'comment', 'push', 'ex', 'own', 'suppli', 'god', 'american', 'measur', 'book', 'pull', 'bounc', 'usa', 'smtp', 'wisdom', 'grow', 'earlier', 'bankruptci', 'pipe', 'compel', 'boundari', 'told', 'substanti', 'instantli', 'mac', 'pnumber', 'assumpt', 'prohibit', 'hundr', 'stick', 'fear', 'brows', 'u', 'dream', 'period', 'must', 'numberi', 'hill', 'somewher', 'repeat', 'smoke', 'te', 'tree', 'regular', 'numberdnumb', 'previous', 'trade', 'mostli', 'nigeria', 'repres', 'join', 'destruct', 'stress', 'sorri', 'vacat', 'newsgroup', 'comfort', 'combo', 'doesn', 'effect', 'clean', 'wild', 'largest', 'celebr', 'your', 'explor', 'paper', 'virtual', 'watch', 'safeti', 'il', 'burn', 'not', 'point', 'iirc', 'result', 'perl', 'land', 'lifetim', 'principl', 'receipt', 'logic', 'term', 'dynam', 'court', 'coupl', 'dollar', 'diseas', 'dog', 'sent', 'planet', 'order', 'campaign', 'cover', 'hold', 'taken', 'benefit', 'blue', 'click', 'french', 'drive', 'weapon', 'con', 'basi', 'beta', 'termin', 'deliveri', 'numberk', 'bit', 'authent', 'estim', 'osdn', 'magazin', 'altern', 'rise', 'shown', 'progress', 'mayb', 'partnership', 'mpnumber', 'earli', 'pleas', 'recommend', 'hospit', 'os', 'http', 'evid', 'huge', 'blow', 'wireless', 'southern', 'xnumber', 'toni', 'link', 'strike', 'place', 'miss', 'ed', 'protect', 'absolut', 'angl', 'permiss', 'centuri', 'easili', 'law', 'struggl', 'data', 'archiv', 'fuck', 'va', 'actual', 'promis', 'hall', 'start', 'enough', 'emailaddr', 'editor', 'ok', 'jump', 'child', 'magic', 'africa', 'illeg', 'button', 'domest', 'answer', 'serv', 'devel', 'remot', 'practic', 'set', 'balanc', 'version', 'suse', 'king', 'japan', 'alon', 'project', 'urgent', 'observ', 'count', 'ignor', 'lot', 'perspect', 'busi', 'html', 'charset', 'app', 'j', 'packag', 'avail', 'meatspac', 'shot', 'blog', 'unwant', 'depress', 'blood', 'we', 'attack', 'articl', 'lie', 'look', 'rang', 'brief', 'survei', 'strip', 'herbal', 'xp', 'instal', 'made', 'color', 'recent', 'ship', 'cash', 'militari', 'goe', 'razor', 'conf', 'came', 'en', 'line', 'skill', 'hand', 'minor', 'encod', 'label', 'syndic', 'skeptic', 'exclud', 'instanc', 'antiqu', 'httpaddr\n', 'suspect', 'apolog', 'itself', 'engin', 'call', 'neither', 'tag', 'gatewai', 'rule', 'window', 'annual', 'boot', 'deserv', 'those', 'o', 'amend', 'room', 'studi', 'wall', 'door', 'best', 'worldwid', 'serial', 'optim', 'enjoi', 'lower', 'kit', 'august', 'rohit', 'forum', 'mechan', 'heard', 'commit', 'immedi', 'nb', 'florida', 'deep', 'store', 'final', 'sequenc', 'greater', 'said', 'greg', 'mistak', 'food', 'rc', 'consist', 'virus', 'goal', 'innov', 'subscript', 'technic', 'although', 'sever', 'mlm', 'capabl', 'island', 'addit', 'vs', 'anti', 'ago', 'decad', 'like', 'find', 'tax', 'brother', 'person', 'similar', 'si', 'half', 'disappear', 'ticket', 'rebuild', 'privaci', 'portion', 'unsubscrib', 'choic', 'thirti', 'for', 'scheme', 'bitbitch', 'pioneer', 'reli', 'especi', 'v', 'achiev', 'affect', 'either', 'seen', 'structur', 'crime', 'soni', 'dan', 'power', 'shift', 'perfect', 'exploit', 'doe', 'our', 'action', 'sole', 'morn', 'error', 'properli', 'season', 'site', 'expens', 'stupid', 'three', 'nbsp\n', 'problem', 'hugh', 'mh', 'be', 'prescript', 'previou', 'compar', 'strategi', 'disposit', 'resel', 'hidden', 'exce', 'whatsoev', 'whether', 'hot', 'anumb', 'thursdai', 'tx', 'correctli', 'rent', 'long', 'were', 'sweet', 'european', 'acquisit', 'minim', 'pai', 'chart', 'aa', 'april', 'mile', 'abov', 'chief', 'ap', 'fail', 'super', 'bottom', 'me', 'rais', 'delai', 'babi', 'homeown', 'spring', 'confirm', 'batteri', 'technolog', 'york', 'strongli', 'small', 'gener', 'fairli', 'bad', 'clue', 'citizen', 'handi', 'sidebar', 'kill', 'kevin', 'advertis', 'elimin', 'annoi', 'modul', 'rate', 'folder', 'di', 'form', 'area', 'space', 'critic', 'opinion', 'proof', 'argument', 'f', 'consequ', 'hi', 'minimum', 'locat', 'proprietari', 'truck', 'reduc', 'killer', 'kind', 'statu', 'broker', 'demonstr', 'anonym', 'along', 'connect', 'consult', 'msg', 'llc', 'bb', 'self', 'ceo', 'imagin', 'no', 'useless', 'expert', 'sat', 'content', 'penguin', 'market', 'add', 'littl', 'chicago', 'septemb', 'grant', 'it', 'particularli', 'assembl', 'greet', 'encount', 'employe', 'confidenti', 'invok', 'financ', 'method', 'screen', 'an', 'male', 'readi', 'into', 'numberm', 'earth', 'model', 'int', 'joe', 'shut', 'accur', 'pilot', 'approach', 'commun', 'thousand', 'won', 'realiti', 'wire', 'admit', 'wish', 'typic', 'familiar', 'paragraph', 'behavior', 'li', 'g', 'queri', 'mode', 'guidelin', 'remov\n', 'lib', 'despit', 'seek', 'demand', 'expect', 'prompt', 'somebodi', 'unsolicit', 'page', 'char', 'glad', 'credul', 'packard', 'broadcast', 'friend', 'angel', 'prove', 'repositori', 'vehicl', 'whitelist', 'empir', 'envelop', 'size', 'hunt', 'heavi', 'z', 'sleep', 'empti', 'pc', 'catch', 'reliabl', 'should', 'rose', 'stabil', 'delet', 'wave', 'bush', 'home', 'june', 'republ', 'thoma', 'necessari', 'author', 'style', 'most', 'keyboard', 'advis', 'under', 'databas', 'displai', 'instant', 'auto', 'numberpm', 'tm', 'obtain', 'english', 'polici', 'endors', 'bless', 'biggest', 'visa', 'awai', 'switch', 'intern', 'pictur', 'terribl', 'adjust', 'conflict', 'aim', 'ha', 'attempt', 'solut', 'dump', 'doubl', 'former', 'cold', 'swap', 'boss', 'heck', 'texa', 'physic', 'he', 'complain', 'touch', 'pgp', 'leader', 'continu', 'origin', 'ill', 'heaven', 'shoot', 'ebai', 'ran', 'presid', 'sinc', 'stop', 'who', 'sendmail', 'bin', 'sender', 'build', 'wast', 'laugh', 'die', 'picasso', 'beyond', 'bind', 'man', 'cancer', 'histor', 'cool', 'messag', 'basenumb', 'tcl', 'just', 'block', 'budget', 'spin', 'liter', 'bell', 'note', 'approv', 'numberrd', 'prospect', 'arrai', 'began', 'bob', 'kid', 'edificio', 'disclaim', 'enemi', 'win', 'planta', 'apt', 'conclus', 'extra', 'corpor', 'met', 'maintain', 'anyth', 'begin', 'jabber', 'discoveri', 'vision', 'corner', 'consolid', 'floppi', 'stream', 'light', 'muscl', 'index', 'hair', 'compress', 'ii', 'gmt', 'outstand', 'word', 'soon', 'corpu', 'introduc', 'kindli', 'increas', 'await', 'section', 'show', 'inumb', 'cf', 'intel', 'member', 'flat', 'among', 'rapid', 'sea', 'adam', 'take', 'camera', 'children', 'kick', 'applic', 'grand', 'justin', 'women', 'loan', 'know', 'repair', 'devic', 'commerci', 'more', 'produc', 'peter', 'move', 'invent', 'haven', 'group', 'py', 'happier', 'provid', 'issu', 'confus', 'ip', 'complet', 'shouldn', 'activ', 'newslett', 'accord', 'wai', 'tom', 'there', 'normal', 'motiv', 'foot', 'themselv', 'embed', 'notif', 'column', 'dark', 'particular', 'approxim', 'scott', 'strong', 'total', 'ahead', 'lnumber', 'next', 'scientif', 'larger', 'four', 'him', 'parti', 'given', 'bound', 'opposit', 'mine', 'contain', 'emot', 'secret', 'shape', 'th', 'rout', 'incom', 'norton', 'control', 'pressur', 'dave', 'wear', 'mountain', 'support', 'onlin', 'output', 'tomorrow', 'fast', 'sincer', 'player', 'nobodi', 'multi', 'po', 'storag', 'contract', 'scientist', 'evil', 'pa', 'better', 'song', 'latter', 'url', 'ps', 'while', 'viru', 'cut', 'hettinga', 'interest', 'satellit', 'eas', 'will', 'from', 'van', 'hide', 'freshrpm', 'ie', 'explicitli', 'financi', 'amp', 'duplic', 'as', 'sex', 'compat', 'numer', 'odd', 'percentag', 'mondai', 'hadn', 'junk', 'british', 'spec', 'discount', 'cd', 'tech', 'post', 'voic', 'ing', 'conserv', 'fnumber', 'piec', 'promot', 'unix', 'drag', 'talk', 'date', 'surpris', 'educ', 'would', 'compani', 'ensur', 'recogn', 'at', 'retriev', 'violat', 'websit', 'fulli', 'threat', 'creator', 'job', 'attain', 'martin', 'pass', 'acknowledg', 'classic', 'download', 'overnight', 'cheap', 'time', 'guido', 'these', 'crash', 'come', 'exit', 'flash', 'numberc', 'india', 'brand', 'reader', 'command', 'kept', 'im', 'georg', 'low', 'img', 'rob', 'collector', 'loop', 'librari', 'directori', 'x', 'edg', 'rush', 'older', 'there\n', 'appar', 'return', 'bui', 'attach', 'stock', 'inexpens', 'some', 'lift', 'formula', 'master', 'dsl', 'saw', 'felt', 'convent', 'chip', 'orient', 'guid', 'legisl', 'q', 'shall', 'sober', 'partit', 'design', 'string', 'feder', 'desk', 'log', 'inform', 'statement', 'insid', 'full', 'iso', 'becam', 'loss', 'giant', 'statist', 'info', 'inde', 'intend', 'sundai', 'tri', 'vipul', 'farquhar', 'belong', 'artist', 'symbol', 'stephen', 'highli', 'proper', 't', 'cc', 'random', 'faster', 'doctor', 'compens', 'femal', 'ever', 'draw', 'fun', 'honor', 'convinc', 'elsewher', 'flow', 'notifi', 'held']
    # ^ copied from terminal output from q1.py

    weight_mapping = {}
    index = 0
    for w in model.w:
        weight_mapping[w] = index
        index += 1
    
    all_weights = model.w
    all_weights.sort()
    final_positive = all_weights[0:15]
    final_negative = all_weights[len(all_weights)-16: len(all_weights)-1]
    final, cor_weights = [], []
    for i in final_positive:
        final.append(original_list[weight_mapping[i]])
        cor_weights.append("{:.3f}".format(i))
    for i in final_negative:
        final.append(original_list[weight_mapping[i]])
        cor_weights.append("{:.3f}".format(i))
    # print(final_positive)
    # print(final_negative)
    # print(cor_weights)
    # print(final)

    ## For Q3 Only
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    yTrain = np.array(yTrain).ravel()
    # NB
    nb_classifier = MultinomialNB()
    nb_classifier.fit(xTrain, yTrain)

    yHat = nb_classifier.predict(xTest)
    yHat_train = nb_classifier.predict(xTrain)
    accuracy = accuracy_score(yTest, yHat)
    accuracy_train = accuracy_score(yTrain, yHat_train)

    print("Test Accuracy Naive Bayes:", accuracy, 1-accuracy)
    print("Training Accuracy Naive Bayes:", accuracy_train, 1-accuracy_train)
    # LR
    logistic_reg = LogisticRegression()
    logistic_reg.fit(xTrain, yTrain)

    yHat = logistic_reg.predict(xTest)
    yHat_train = logistic_reg.predict(xTrain)

    accuracy = accuracy_score(yTest, yHat)
    accuracy_train = accuracy_score(yTrain, yHat_train)

    print("Test Accuracy Logistic Regression:", accuracy, 1-accuracy)
    print("Training Accuracy Logistic Regression:", accuracy_train, 1-accuracy_train)

if __name__ == "__main__":
    main()

# python perceptron.py xTrain.csv yTrain.csv xTest.csv yTest.csv 50
# python perceptron.py xTrain-c.csv yTrain-c.csv xTest-c.csv yTest-c.csv 50