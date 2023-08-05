import asyncio

from mirai_core import Bot, Updater
from mirai_core.models.Event import Message, BotOnlineEvent
from mirai_core.models.Types import MessageType
from mirai_core.models.Message import MessageChain, Image, Plain, At, AtAll, Face, Source, Quote, FlashImage

from unified_message_relay.Core.UMRType import ChatType, UnifiedMessage, MessageEntity, EntityType, ChatAttribute
from unified_message_relay.Core.UMRMessageRelation import set_ingress_message_id, set_egress_message_id
from unified_message_relay.Core.UMRDriver import BaseDriverMixin
from unified_message_relay.Core import UMRDriver
from unified_message_relay.Core import UMRLogging
from unified_message_relay.Core import UMRConfig
from typing import Union, Dict, List, Tuple
from typing_extensions import Literal
from pydantic import Field
import threading

qq_emoji_list = {  # created by JogleLew and jqqqqqqqqqq, optimized based on Tim's emoji support
    0:   '😮',
    1:   '😣',
    2:   '😍',
    3:   '😳',
    4:   '😎',
    5:   '😭',
    6:   '☺️',
    7:   '😷',
    8:   '😴',
    9:   '😭',
    10:  '😰',
    11:  '😡',
    12:  '😝',
    13:  '😃',
    14:  '🙂',
    15:  '🙁',
    16:  '🤓',
    17:  '[Empty]',
    18:  '😤',
    19:  '😨',
    20:  '😏',
    21:  '😊',
    22:  '🙄',
    23:  '😕',
    24:  '🤤',
    25:  '😪',
    26:  '😨',
    27:  '😓',
    28:  '😬',
    29:  '🤑',
    30:  '✊',
    31:  '😤',
    32:  '🤔',
    33:  '🤐',
    34:  '😵',
    35:  '😩',
    36:  '💣',
    37:  '💀',
    38:  '🔨',
    39:  '👋',
    40:  '[Empty]',
    41:  '😮',
    42:  '💑',
    43:  '🕺',
    44:  '[Empty]',
    45:  '[Empty]',
    46:  '🐷',
    47:  '[Empty]',
    48:  '[Empty]',
    49:  '🤷',
    50:  '[Empty]',
    51:  '[Empty]',
    52:  '[Empty]',
    53:  '🎂',
    54:  '⚡',
    55:  '💣',
    56:  '🔪',
    57:  '⚽️',
    58:  '[Empty]',
    59:  '💩',
    60:  '☕️',
    61:  '🍚',
    62:  '[Empty]',
    63:  '🌹',
    64:  '🥀',
    65:  '[Empty]',
    66:  '❤️',
    67:  '💔️',
    68:  '[Empty]',
    69:  '🎁',
    70:  '[Empty]',
    71:  '[Empty]',
    72:  '[Empty]',
    73:  '[Empty]',
    74:  '🌞️',
    75:  '🌃',
    76:  '👍',
    77:  '👎',
    78:  '🤝',
    79:  '✌️',
    80:  '[Empty]',
    81:  '[Empty]',
    82:  '[Empty]',
    83:  '[Empty]',
    84:  '[Empty]',
    85:  '🥰',
    86:  '[怄火]',
    87:  '[Empty]',
    88:  '[Empty]',
    89:  '🍉',
    90:  '[Empty]',
    91:  '[Empty]',
    92:  '[Empty]',
    93:  '[Empty]',
    94:  '[Empty]',
    95:  '[Empty]',
    96:  '😅',
    97:  '[擦汗]',
    98:  '[抠鼻]',
    99:  '👏',
    100: '[糗大了]',
    101: '😏',
    102: '😏',
    103: '😏',
    104: '🥱',
    105: '[鄙视]',
    106: '😭',
    107: '😭',
    108: '[阴险]',
    109: '😚',
    110: '🙀',
    111: '[可怜]',
    112: '🔪',
    113: '🍺',
    114: '🏀',
    115: '🏓',
    116: '❤️',
    117: '🐞',
    118: '[抱拳]',
    119: '[勾引]',
    120: '✊',
    121: '[差劲]',
    122: '🤟',
    123: '🚫',
    124: '👌',
    125: '[转圈]',
    126: '[磕头]',
    127: '[回头]',
    128: '[跳绳]',
    129: '👋',
    130: '[激动]',
    131: '[街舞]',
    132: '😘',
    133: '[左太极]',
    134: '[右太极]',
    135: '[Empty]',
    136: '[双喜]',
    137: '🧨',
    138: '🏮',
    139: '💰',
    140: '[K歌]',
    141: '🛍️',
    142: '📧',
    143: '[帅]',
    144: '👏',
    145: '🙏',
    146: '[爆筋]',
    147: '🍭',
    148: '🍼',
    149: '[下面]',
    150: '🍌',
    151: '🛩',
    152: '🚗',
    153: '🚅',
    154: '[车厢]',
    155: '[高铁右车头]',
    156: '🌥',
    157: '下雨',
    158: '💵',
    159: '🐼',
    160: '💡',
    161: '[风车]',
    162: '⏰',
    163: '🌂',
    164: '[彩球]',
    165: '💍',
    166: '🛋',
    167: '[纸巾]',
    168: '💊',
    169: '🔫',
    170: '🐸',
    171: '🍵',
    172: '[眨眼睛]',
    173: '😭',
    174: '[无奈]',
    175: '[卖萌]',
    176: '[小纠结]',
    177: '[喷血]',
    178: '[斜眼笑]',
    179: '[doge]',
    180: '[惊喜]',
    181: '[骚扰]',
    182: '😹',
    183: '[我最美]',
    184: '🦀',
    185: '[羊驼]',
    186: '[Empty]',
    187: '👻',
    188: '🥚',
    189: '[Empty]',
    190: '🌼',
    191: '[Empty]',
    192: '🧧',
    193: '😄',
    194: '😞',
    195: '[Empty]',
    196: '[Empty]',
    197: '[冷漠]',
    198: '[呃]',
    199: '👍',
    200: '👋',
    201: '👍',
    202: '[无聊]',
    203: '[托脸]',
    204: '[吃]',
    205: '💐',
    206: '😨',
    207: '[花痴]',
    208: '[小样儿]',
    209: '[Empty]',
    210: '😭',
    211: '[我不看]',
    212: '[托腮]',
    213: '[Empty]',
    214: '😙',
    215: '[糊脸]',
    216: '[拍头]',
    217: '[扯一扯]',
    218: '[舔一舔]',
    219: '[蹭一蹭]',
    220: '[拽炸天]',
    221: '[顶呱呱]',
    222: '🤗',
    223: '[暴击]',
    224: '🔫',
    225: '[撩一撩]',
    226: '[拍桌]',
    227: '👏',
    228: '[恭喜]',
    229: '🍻',
    230: '[嘲讽]',
    231: '[哼]',
    232: '[佛系]',
    233: '[掐一掐]',
    234: '😮',
    235: '[颤抖]',
    236: '[啃头]',
    237: '[偷看]',
    238: '[扇脸]',
    239: '[原谅]',
    240: '[喷脸]',
    241: '🎂',
    242: '[Empty]',
    243: '[Empty]',
    244: '[Empty]',
    245: '[Empty]',
    246: '[Empty]',
    247: '[Empty]',
    248: '[Empty]',
    249: '[Empty]',
    250: '[Empty]',
    251: '[Empty]',
    252: '[Empty]',
    253: '[Empty]',
    254: '[Empty]',
    255: '[Empty]',
}

# original text copied from Tim
qq_emoji_text_list = {
    0:   '[惊讶]',
    1:   '[撇嘴]',
    2:   '[色]',
    3:   '[发呆]',
    4:   '[得意]',
    5:   '[流泪]',
    6:   '[害羞]',
    7:   '[闭嘴]',
    8:   '[睡]',
    9:   '[大哭]',
    10:  '[尴尬]',
    11:  '[发怒]',
    12:  '[调皮]',
    13:  '[呲牙]',
    14:  '[微笑]',
    15:  '[难过]',
    16:  '[酷]',
    17:  '[Empty]',
    18:  '[抓狂]',
    19:  '[吐]',
    20:  '[偷笑]',
    21:  '[可爱]',
    22:  '[白眼]',
    23:  '[傲慢]',
    24:  '[饥饿]',
    25:  '[困]',
    26:  '[惊恐]',
    27:  '[流汗]',
    28:  '[憨笑]',
    29:  '[悠闲]',
    30:  '[奋斗]',
    31:  '[咒骂]',
    32:  '[疑问]',
    33:  '[嘘]',
    34:  '[晕]',
    35:  '[折磨]',
    36:  '[衰]',
    37:  '[骷髅]',
    38:  '[敲打]',
    39:  '[再见]',
    40:  '[Empty]',
    41:  '[发抖]',
    42:  '[爱情]',
    43:  '[跳跳]',
    44:  '[Empty]',
    45:  '[Empty]',
    46:  '[猪头]',
    47:  '[Empty]',
    48:  '[Empty]',
    49:  '[拥抱]',
    50:  '[Empty]',
    51:  '[Empty]',
    52:  '[Empty]',
    53:  '[蛋糕]',
    54:  '[闪电]',
    55:  '[炸弹]',
    56:  '[刀]',
    57:  '[足球]',
    58:  '[Empty]',
    59:  '[便便]',
    60:  '[咖啡]',
    61:  '[饭]',
    62:  '[Empty]',
    63:  '[玫瑰]',
    64:  '[凋谢]',
    65:  '[Empty]',
    66:  '[爱心]',
    67:  '[心碎]',
    68:  '[Empty]',
    69:  '[礼物]',
    70:  '[Empty]',
    71:  '[Empty]',
    72:  '[Empty]',
    73:  '[Empty]',
    74:  '[太阳]',
    75:  '[月亮]',
    76:  '[赞]',
    77:  '[踩]',
    78:  '[握手]',
    79:  '[胜利]',
    80:  '[Empty]',
    81:  '[Empty]',
    82:  '[Empty]',
    83:  '[Empty]',
    84:  '[Empty]',
    85:  '[飞吻]',
    86:  '[怄火]',
    87:  '[Empty]',
    88:  '[Empty]',
    89:  '[西瓜]',
    90:  '[Empty]',
    91:  '[Empty]',
    92:  '[Empty]',
    93:  '[Empty]',
    94:  '[Empty]',
    95:  '[Empty]',
    96:  '[冷汗]',
    97:  '[擦汗]',
    98:  '[抠鼻]',
    99:  '[鼓掌]',
    100: '[糗大了]',
    101: '[坏笑]',
    102: '[左哼哼]',
    103: '[右哼哼]',
    104: '[哈欠]',
    105: '[鄙视]',
    106: '[委屈]',
    107: '[快哭了]',
    108: '[阴险]',
    109: '[亲亲]',
    110: '[吓]',
    111: '[可怜]',
    112: '[菜刀]',
    113: '[啤酒]',
    114: '[篮球]',
    115: '[乒乓]',
    116: '[示爱]',
    117: '[瓢虫]',
    118: '[抱拳]',
    119: '[勾引]',
    120: '[拳头]',
    121: '[差劲]',
    122: '[爱你]',
    123: '[NO]',
    124: '[OK]',
    125: '[转圈]',
    126: '[磕头]',
    127: '[回头]',
    128: '[跳绳]',
    129: '[挥手]',
    130: '[激动]',
    131: '[街舞]',
    132: '[献吻]',
    133: '[左太极]',
    134: '[右太极]',
    135: '[Empty]',
    136: '[双喜]',
    137: '[鞭炮]',
    138: '[灯笼]',
    139: '[发财]',
    140: '[K歌]',
    141: '[购物]',
    142: '[邮件]',
    143: '[帅]',
    144: '[喝彩]',
    145: '[祈祷]',
    146: '[爆筋]',
    147: '[棒棒糖]',
    148: '[喝奶]',
    149: '[下面]',
    150: '[香蕉]',
    151: '[飞机]',
    152: '[开车]',
    153: '[高铁左车头]',
    154: '[车厢]',
    155: '[高铁右车头]',
    156: '[多云]',
    157: '[下雨]',
    158: '[钞票]',
    159: '[熊猫]',
    160: '[灯泡]',
    161: '[风车]',
    162: '[闹钟]',
    163: '[打伞]',
    164: '[彩球]',
    165: '[钻戒]',
    166: '[沙发]',
    167: '[纸巾]',
    168: '[药]',
    169: '[手枪]',
    170: '[青蛙]',
    171: '[茶]',
    172: '[眨眼睛]',
    173: '[泪奔]',
    174: '[无奈]',
    175: '[卖萌]',
    176: '[小纠结]',
    177: '[喷血]',
    178: '[斜眼笑]',
    179: '[doge]',
    180: '[惊喜]',
    181: '[骚扰]',
    182: '[笑哭]',
    183: '[我最美]',
    184: '[河蟹]',
    185: '[羊驼]',
    186: '[Empty]',
    187: '[幽灵]',
    188: '[蛋]',
    189: '[Empty]',
    190: '[菊花]',
    191: '[Empty]',
    192: '[红包]',
    193: '[大笑]',
    194: '[不开心]',
    195: '[Empty]',
    196: '[Empty]',
    197: '[冷漠]',
    198: '[呃]',
    199: '[好棒]',
    200: '[拜托]',
    201: '[点赞]',
    202: '[无聊]',
    203: '[托脸]',
    204: '[吃]',
    205: '[送花]',
    206: '[害怕]',
    207: '[花痴]',
    208: '[小样儿]',
    209: '[Empty]',
    210: '[飙泪]',
    211: '[我不看]',
    212: '[托腮]',
    213: '[Empty]',
    214: '[啵啵]',
    215: '[糊脸]',
    216: '[拍头]',
    217: '[扯一扯]',
    218: '[舔一舔]',
    219: '[蹭一蹭]',
    220: '[拽炸天]',
    221: '[顶呱呱]',
    222: '[抱抱]',
    223: '[暴击]',
    224: '[开枪]',
    225: '[撩一撩]',
    226: '[拍桌]',
    227: '[拍手]',
    228: '[恭喜]',
    229: '[干杯]',
    230: '[嘲讽]',
    231: '[哼]',
    232: '[佛系]',
    233: '[掐一掐]',
    234: '[惊呆]',
    235: '[颤抖]',
    236: '[啃头]',
    237: '[偷看]',
    238: '[扇脸]',
    239: '[原谅]',
    240: '[喷脸]',
    241: '[生日快乐]',
    242: '[Empty]',
    243: '[Empty]',
    244: '[Empty]',
    245: '[Empty]',
    246: '[Empty]',
    247: '[Empty]',
    248: '[Empty]',
    249: '[Empty]',
    250: '[Empty]',
    251: '[Empty]',
    252: '[Empty]',
    253: '[Empty]',
    254: '[Empty]',
    255: '[Empty]',
}

qq_sface_list = {
    1:  '[拜拜]',
    2:  '[鄙视]',
    3:  '[菜刀]',
    4:  '[沧桑]',
    5:  '[馋了]',
    6:  '[吃惊]',
    7:  '[微笑]',
    8:  '[得意]',
    9:  '[嘚瑟]',
    10: '[瞪眼]',
    11: '[震惊]',
    12: '[鼓掌]',
    13: '[害羞]',
    14: '[好的]',
    15: '[惊呆了]',
    16: '[静静看]',
    17: '[可爱]',
    18: '[困]',
    19: '[脸红]',
    20: '[你懂的]',
    21: '[期待]',
    22: '[亲亲]',
    23: '[伤心]',
    24: '[生气]',
    25: '[摇摆]',
    26: '[帅]',
    27: '[思考]',
    28: '[震惊哭]',
    29: '[痛心]',
    30: '[偷笑]',
    31: '[挖鼻孔]',
    32: '[抓狂]',
    33: '[笑着哭]',
    34: '[无语]',
    35: '[捂脸]',
    36: '[喜欢]',
    37: '[笑哭]',
    38: '[疑惑]',
    39: '[赞]',
    40: '[眨眼]'
}


class MiraiDriverConfig(UMRConfig.BaseDriverConfig):
    Base: Literal['Mirai']
    Account: int
    Host: str
    Port: int = Field(18080, ge=0, le=65535)
    AuthKey: str
    NameforPrivateChat: bool = True
    NameforGroupChat: bool = True


UMRConfig.register_driver_config(MiraiDriverConfig)


class MiraiDriver(BaseDriverMixin):
    def __init__(self, name):
        super().__init__(name)

        self.name = name
        self.logger = UMRLogging.get_logger('Mirai')
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.loop.set_exception_handler(self.handle_exception)

        self.image_cache = dict()
        self.config: MiraiDriverConfig = UMRConfig.config.Driver[self.name]

        self.qq = self.config.Account
        auth_key = self.config.AuthKey
        host = self.config.Host
        port = self.config.Port

        self.bot = Bot(self.qq, host, port, auth_key, loop=self.loop)
        self.updater = Updater(self.bot)

        @self.updater.add_handler(BotOnlineEvent)
        async def friend_message(event: BotOnlineEvent):
            print(111)

        @self.updater.add_handler(Message)
        async def friend_message(event: Message):

            if event.type == MessageType.GROUP.value:
                chat_type = ChatType.GROUP
                username = event.member.memberName
                chat_id = event.member.group.id
                user_id = event.member.id
            elif event.type == MessageType.FRIEND.value:
                chat_type = ChatType.PRIVATE
                username = event.friend.remark or event.friend.nickname
                chat_id = event.friend.id
                user_id = event.friend.id
            else:
                chat_type = ChatType.GROUP
                username = event.member.memberName
                chat_id = event.member.id
                user_id = event.member.id

            self.logger.debug(f"[{event.type}][{chat_id}][{username}({user_id})]: " +
                              str(event.messageChain))

            message_id = event.messageChain.get_source().id

            set_ingress_message_id(src_platform=self.name,
                                   src_chat_id=chat_id,
                                   src_chat_type=chat_type,
                                   src_message_id=message_id,
                                   user_id=user_id)

            if event.type == MessageType.TEMP:
                username += ' [TempMessage]'
            unified_message_list = await self.parse_message(message_chain=event.messageChain,
                                                            chat_id=chat_id,
                                                            chat_type=chat_type,
                                                            username=username,
                                                            user_id=user_id,
                                                            message_id=message_id)
            try:
                for message in unified_message_list:
                    await self.receive(message)
            except Exception as e:
                self.logger.exception('unhandled exception:', exc_info=e)

    async def parse_message(self,
                            message_chain: MessageChain,
                            chat_id: int,
                            chat_type: ChatType,
                            username: str,
                            message_id: int,
                            user_id: int):
        message_list = list()
        unified_message = UnifiedMessage(platform=self.name,
                                         chat_id=chat_id,
                                         chat_type=chat_type,
                                         name=username,
                                         user_id=user_id,
                                         message_id=message_id)
        quote = message_chain.get_quote()
        if quote:
            unified_message.chat_attrs.reply_to = ChatAttribute(platform=self.name,
                                                                chat_id=chat_id,
                                                                chat_type=chat_type,
                                                                user_id=quote.senderId,
                                                                name='unknown',
                                                                message_id=quote.id)

        for m in message_chain[1:]:
            if isinstance(m, (Image, FlashImage)):
                # message not empty or contained a image, append to list
                if unified_message.image or unified_message.text:
                    message_list.append(unified_message)
                    unified_message = UnifiedMessage(platform=self.name,
                                                     chat_id=chat_id,
                                                     chat_type=chat_type,
                                                     name=username,
                                                     user_id=user_id,
                                                     message_id=message_id)
                unified_message.image = m.url
                self.logger.debug(f'Received image: [{m.imageId}]')

            elif isinstance(m, Plain):
                unified_message.text += m.text
            elif isinstance(m, At):

                at_user_text = m.display
                unified_message.text_entities.append(
                    MessageEntity(start=len(unified_message.text),
                                  end=len(unified_message.text) + len(at_user_text),
                                  entity_type=EntityType.BOLD))
                unified_message.text += at_user_text
            elif isinstance(m, AtAll):

                at_user_text = '[@All]'
                unified_message.text_entities.append(
                    MessageEntity(start=len(unified_message.text),
                                  end=len(unified_message.text) + len(at_user_text),
                                  entity_type=EntityType.BOLD))
                unified_message.text += at_user_text
            elif isinstance(m, Face):
                qq_face = int(m.faceId) & 255
                if qq_face in qq_emoji_list:
                    unified_message.text += qq_emoji_list[qq_face]
                else:
                    unified_message.text += '\u2753'  # ❓
            elif isinstance(m, Source):
                pass
            elif isinstance(m, Quote):
                pass
            else:
                unified_message.text += str(m)
                self.logger.debug(f'Unhandled message type: {str(m)}')

        message_list.append(unified_message)
        return message_list

    def start(self):
        def run():
            nonlocal self
            asyncio.set_event_loop(self.loop)
            self.logger.debug(f'Starting Session for {self.name}')

            self.loop.create_task(self.updater.run_task())
            self.loop.run_forever()

        t = threading.Thread(target=run)
        t.daemon = True
        UMRDriver.threads.append(t)
        t.start()

        self.logger.debug(f'Finished initialization for {self.name}')

    async def send(self, to_chat: Union[int, str], chat_type: ChatType, messsage: UnifiedMessage):
        """
        decorator for send new message
        :return:
        """
        self.logger.debug('calling real send')
        return asyncio.run_coroutine_threadsafe(self._send(to_chat, chat_type, messsage), self.loop)

    async def _send(self, to_chat: int, chat_type: ChatType, message: UnifiedMessage):
        """
        decorator for send new message
        :return:
        """
        messages = list()

        if (chat_type == ChatType.PRIVATE and self.config.NameforPrivateChat) or \
                (chat_type in (ChatType.GROUP, ChatType.DISCUSS) and self.config.NameforGroupChat):
            # name logic
            if message.chat_attrs.name:
                messages.append(Plain(text=message.chat_attrs.name))
            # if message.chat_attrs.reply_to:
            #     messages.append(Plain(text=' (➡️️' + message.chat_attrs.reply_to.name + ')'))
            if message.chat_attrs.forward_from:
                messages.append(Plain(text=' (️️↩️' + message.chat_attrs.forward_from.name + ')'))
            if message.chat_attrs.name:
                messages.append(Plain(text=': '))

        # at user
        if not message.send_action.message_id and message.send_action.user_id:
            messages.append(At(target=message.send_action.user_id))
            messages.append(Plain(text=' '))

        if message.text:
            messages.append(Plain(text=message.text))

        if message.image:
            # if chat_type == ChatType.PRIVATE:
            #     image_type = TargetType.Friend
            # else:
            #     image_type = TargetType.Group
            image_id = self.image_cache.get((chat_type, message.image))
            if image_id:
                image = Image(imageId=image_id)
            else:
                image = Image(path=message.image)
                # image = await self.bot.upload_image(image_type=image_type, image_path=message.image)
                # self.image_cache[(image_type, message.image)] = image.imageId
            messages.append(image)
            self.logger.info('If QQ does not receive this message, '
                             'your account might be suspected of being compromised by Tencent')

        quote = message.send_action.message_id or None
        temp_group = None
        if chat_type == ChatType.PRIVATE:
            message_type = MessageType.FRIEND
        else:
            if '[TempMessage]' in message.chat_attrs.name:
                message_type = MessageType.Temp
                temp_group = message.chat_attrs.chat_id
            else:
                message_type = MessageType.GROUP

        egress_message = await self.bot.send_message(
            target=to_chat,
            message_type=message_type,
            message=messages,
            temp_group=temp_group,
            quote_source=quote
        )

        for i in messages:
            if isinstance(i, Image):
                self.image_cache[(chat_type, message.image)] = i.imageId
                break

        if message.chat_attrs:
            set_egress_message_id(src_platform=message.chat_attrs.platform,
                                  src_chat_id=message.chat_attrs.chat_id,
                                  src_chat_type=message.chat_attrs.chat_type,
                                  src_message_id=message.chat_attrs.message_id,
                                  dst_platform=self.name,
                                  dst_chat_id=to_chat,
                                  dst_chat_type=chat_type,
                                  dst_message_id=egress_message.messageId,
                                  user_id=self.qq)

    async def is_group_admin(self, chat_id: int, chat_type: ChatType, user_id: int):
        if chat_type != ChatType.GROUP:
            return False
        return False

    async def is_group_owner(self, chat_id: int, chat_type: ChatType, user_id: int):
        if chat_type != ChatType.GROUP:
            return False
        return False

    def handle_exception(self, loop, context):
        # context["message"] will always be there; but context["exception"] may not
        msg = context.get("exception", context["message"])
        self.logger.exception('Unhandled exception: ', exc_info=msg)


UMRDriver.register_driver('Mirai', MiraiDriver)
