import time

class JavaLCG(object):

  __SEED_LENGTH = 48

  def __init__(self, seed=int(time.time() * 1000)):
    self.seed = seed
    self.set_seed(self.seed)

  def set_seed(self, seed):
    self.seed = (self.seed ^ 0x5DEECE66DL) & ((1 << JavaLCG.__SEED_LENGTH) - 1);

  def get_bits(self, bits=32):
    """Returns the next "bits" from the LCG
    Equivalent to
    import java.util.Random;
    Random r = new Random(5);
    int i1 = r.nextInt();
    int i2 = r.nextInt();
    >>> r = JavaLCG(seed=5)
    >>> it = iter(r.get_bits(32))
    >>> i1 = it.next()
    >>> print(hex(i1))
    0xbb0359bfL
    >>> print(hex(r.seed))
    0xbb0359bf8a53L
    >>> i2 = it.next()
    >>> print(hex(i2))
    0x2d35cb58L
    >>> print(hex(r.seed))
    0x2d35cb587762L
    """
    while True:
      self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << JavaLCG.__SEED_LENGTH) - 1)
      yield self.seed >> (JavaLCG.__SEED_LENGTH - bits)

  @staticmethod
  def bruteforce_seed(i1, i2):
    """
    >>> i1 = 0xbb0359bfL
    >>> i2 = 0x2d35cb58L
    >>> seed = JavaLCG.bruteforce_seed(0xbb0359bfL, 0x2d35cb58L)
    >>> print(hex(seed))
    0xbb0359bf8a53
    >>> r = JavaLCG()
    >>> r.seed = seed
    >>> iter(r.get_bits()).next() == i2
    True
    """
    # Only 32 bits of seed are exposed. Leaves 48 - 32 = 16 bits to find
    missing_bits = 16
    i1 <<= missing_bits
    seed = 0
    for seed in xrange(i1, i1 + 2**missing_bits):
      tmp = (seed  * 0x5DEECE66D + 0xB) & ((1 << JavaLCG.__SEED_LENGTH) - 1)
      if tmp >> 16 == i2:
        break
    return seed

  def get_next_values(self, num_values=10, num_bits=32):
    """
    >>> r = JavaLCG()
    >>> r.seed = 0xbb0359bf8a53
    >>> next_vals = r.get_next_values(5)
    >>> next_vals[0] == 0x2d35cb58
    True
    >>> print(next_vals)
    [758500184L, 379066948L, 2627738848L, 2099829013L, 4058635210L]
    """
    it = iter(self.get_bits(num_bits))
    return [it.next() for _ in xrange(num_values)]
    
if __name__ == "__main__":
  import doctest
  doctest.testmod()
