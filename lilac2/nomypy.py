# type: ignore

class SumType:
  _intermediate = True

  def __init__(self) -> None:
    if self.__class__.__dict__.get('_intermediate', False):
      raise TypeError('use subclasses')

  def __init_subclass__(cls):
    if not cls.__dict__.get('_intermediate', False):
      setattr(cls.__mro__[1], cls.__name__, cls)

  def __repr__(self) -> str:
    cname = __class__.__name__
    name = self.__class__.__name__
    if e := self._extra_info():
      return f'<{cname}.{name}: {e}>'
    else:
      return f'<{cname}.{name}>'

  def _extra_info(self):
    return ''

class BuildResult(SumType):
  _intermediate = True
  rusage = None

  def __bool__(self) -> bool:
    return self.__class__ in [self.successful, self.staged]

  def _extra_info(self):
    return f'rusage={self.rusage}'

class successful(BuildResult):
  pass

class staged(BuildResult):
  pass

class failed(BuildResult):
  def __init__(self, exc: Exception) -> None:
    self.exc = exc

  def _extra_info(self) -> str:
    return f'{self.exc!r}; {super()._extra_info()}'

class skipped(BuildResult):
  def __init__(self, reason: str) -> None:
    self.reason = reason

  def _extra_info(self) -> str:
    return f'{self.reason!r}; {super()._extra_info()}'

del successful, staged, failed, skipped

class BuildReason(SumType):
  _intermediate = True

  def to_dict(self) -> str:
    d = {k: v for k, v in self.__dict__.items()
         if not k.startswith('_')}
    d['name'] = self.__class__.__name__
    return d

class NvChecker(BuildReason):
  def __init__(self, items: list[tuple[int, str]]) -> None:
    '''items: list of (nvchecker entry index, source name)'''
    self.items = items

  def _extra_info(self) -> str:
    return repr(self.items)

class UpdatedFailed(BuildReason):
  '''previously failed package gets updated'''

class UpdatedPkgrel(BuildReason): pass

class Depended(BuildReason):
  def __init__(self, depender):
    self.depender = depender

  def _extra_info(self) -> str:
    return self.depender

# TODO
class DepsRecovered(BuildReason):
  def __init__(self, deps: list[str]) -> None:
    self.deps = deps

class Cmdline(BuildReason): pass

del NvChecker, UpdatedFailed, UpdatedPkgrel, Depended, DepsRecovered, Cmdline
