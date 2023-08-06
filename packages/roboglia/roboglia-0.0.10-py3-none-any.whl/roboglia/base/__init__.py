from ..utils.factory import register_class

from .bus import BaseBus                        # noqa: 401
from .bus import FileBus                        # noqa: 401
from .bus import ShareableBus                   # noqa: 401
from .bus import ShareableFileBus               # noqa: 401


from .register import BaseRegister              # noqa: 401
from .register import BoolRegister              # noqa: 401
from .register import RegisterWithConversion    # noqa: 401
from .register import RegisterWithThreshold     # noqa: 401

from .device import BaseDevice                  # noqa: 401

from .joint import Joint                        # noqa: 401
from .joint import JointPV                      # noqa: 401
from .joint import JointPVL                     # noqa: 401

from .thread import BaseThread                  # noqa: 401
from .thread import BaseLoop                    # noqa: 401

from .sync import BaseSync                      # noqa: 401
from .sync import BaseReadSync                  # noqa: 401
from .sync import BaseWriteSync                 # noqa: 401

from .robot import BaseRobot                    # noqa: 401

register_class(FileBus)
register_class(ShareableFileBus)

register_class(BaseRegister)
register_class(RegisterWithConversion)
register_class(RegisterWithThreshold)
register_class(BoolRegister)

register_class(BaseDevice)

register_class(Joint)
register_class(JointPV)
register_class(JointPVL)

register_class(BaseReadSync)
register_class(BaseWriteSync)
