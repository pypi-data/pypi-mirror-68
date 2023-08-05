from .splice import Splice
from .streamplus import StreamPlus
from bitn import BitBin


class StreamStats(StreamPlus):
    '''
    monitor a live video stream
    '''
    def __init__(self, tsdata, show_null = False):
        #self.PTS= 0.0
        super().__init__(tsdata, show_null)

    def parse_payload(self,payload,pid):
        '''
        Override this method to customize output
        '''
        try:
            tf = Splice(payload,pid=pid, pts=self.PTS)
            print(f'\033[92mSCTE35\033[0m {tf.command.name} @ \033[92m{self.PTS:0.3f}\033[0m')
            if tf.info_section.splice_command_type != 0: tf.show_command()
            print('\n')
            return tf
        except: return False
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        print(f'PTS: \033[92m{self.PTS:0.3f}\033[0m',end = '\r')
        super().parse_tspacket(packet)
        return
       
