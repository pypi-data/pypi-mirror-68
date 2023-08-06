from pathlib import Path
from pyhanlp import HanLP, JClass
from stanza.server import CoreNLPClient

from zwnlp.utils import Backend
from zwutils.logger import logger
LOG = logger(__name__)

class NER(object):
    '''实体识别'''
    def __init__(self, cfg, backend=None):
        self.backend = backend or Backend.corenlp
        self.tags = ['nb', 'nba', 'nbp', 'nf', 'nh', 'nhd', 'nhm', 'ni', 'nic', 'nit', 'nmc',
                    'g', 'gb', 'gbc', 'gc', 'gg', 'gi', 'gm', 'gp',
                    'nr','nr1','nr2','nrf','nrj','nt','ntc','ntcb','ntcf','ntch','nth','nto','nts','ntu']
        self.corenlp_tags = ['PERSON', 'LOCATION', 'ORGANIZATION']
        self.markhtml = '<mark onclick="onEntityClick(this)" data-etype="{nature}">{word}</mark>'
        self.corenlp = None
        if hasattr(cfg, 'corenlp'):
            corenlp_cfg = cfg.corenlp
            classpath_default = str( Path('./corenlp').resolve() )
            classpath_default = '"%s/*"' % classpath_default
            self.corenlp_clspath = corenlp_cfg.get('homepath', classpath_default)
            self.corenlp_memsize = corenlp_cfg.get('memsize', '5G')
            self.corenlp_timeout = corenlp_cfg.get('timeout', 30000)
            self.corenlp_endpoint= corenlp_cfg.get('endpoint', 'http://localhost:9000')

    def __enter__(self):
        if self.backend == Backend.corenlp:
            CoreNLPClient.CHECK_ALIVE_TIMEOUT = 480
            self.corenlp = CoreNLPClient(start_server=False, annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref']
                , endpoint=self.corenlp_endpoint
                , timeout=self.corenlp_timeout
                , memory=self.corenlp_memsize
                , classpath=self.corenlp_clspath)
            # self.corenlp.start()
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def close(self):
        if self.corenlp:
            # self.corenlp.stop()
            self.corenlp = None

    def ner(self, sentences):
        rtn = []
        if Backend.hanlp == self.backend:
            segment = HanLP.newSegment()\
                .enableNameRecognize(True)\
                    .enableTranslatedNameRecognize(True)\
                        .enableOrganizationRecognize(True)\
                            .enablePlaceRecognize(True)
            for sentence in sentences:
                term_list = segment.seg(sentence)
                terms = []
                for o in term_list:
                    word = o.word
                    nature = str(o.nature)
                    if nature in self.tags:
                        terms.append( (word, nature) )
                rtn.append( (sentence, terms) )
        elif Backend.corenlp == self.backend:
            for sentence in sentences:
                ann = self.corenlp.annotate(sentence)
                terms = []
                for s in ann.sentence:
                    term_list = s.token
                    for o in term_list:
                        word = o.word
                        nature = o.ner
                        nature = nature.upper().strip()
                        begchar = o.beginChar
                        endchar = o.endChar
                        if nature in self.corenlp_tags:
                            if len(terms)>0 and terms[-1][1] == nature and terms[-1][3] == begchar-1:
                                _t = terms[-1]
                                terms[-1] = ('%s %s'%(_t[0], word), _t[1], _t[2], endchar)
                                continue
                            terms.append( (word, nature, begchar, endchar) )
                rtn.append( (sentence, terms) )
        return rtn
    
    def htmloutput(self, sentences):
        rtn = []
        arr = self.ner(sentences)
        for a in arr:
            text = a[0] # sentence text
            terms = a[1] # terms in sentence
            text_arr = []
            last_idx = None
            for i,term in enumerate(terms):
                word = term[0]
                nature = term[1]
                # TODO 重复实体名问题
                if self.backend == Backend.corenlp:
                    bef_start = 0 if i==0 else terms[i-1][3]
                    bef_end = term[2]
                    if bef_start != bef_end:
                        text_arr.append(text[bef_start:bef_end])
                    text_arr.append(self.markhtml.format(word=word, nature=nature))
                    last_idx = bef_end + len(word)
                else:
                    text = text.replace(word, self.markhtml.format(word=word, nature=nature))
            if self.backend == Backend.corenlp:
                last = text[last_idx:] if last_idx is not None else text
                text_arr.append(last)
                text = ''.join(text_arr)
            rtn.append(text)
        rtn = ['<p>%s</p>'%s for s in rtn]
        return ''.join(rtn)
