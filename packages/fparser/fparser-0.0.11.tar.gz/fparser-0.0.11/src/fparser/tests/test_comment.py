# Modified work Copyright (c) 2017-2018 Science and Technology
# Facilities Council
# Original work Copyright (c) 1999-2008 Pearu Peterson

# All rights reserved.

# Modifications made as part of the fparser project are distributed
# under the following license:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# --------------------------------------------------------------------

# The original software (in the f2py project) was distributed under
# the following license:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#   a. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   b. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#   c. Neither the name of the F2PY project nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

from fparser.api import parse

def test_comment_lines():
    source_str = '''\
  !comment line 1

!comment line 2
module foo
!comment line 3
subroutine f
!comment line 4
end subroutine f !comment line 5
end module foo
    '''
    tree = parse(source_str, isfree=True, isstrict=False,
                 ignore_comments=False)

    assert str(tree).strip().split('\n')[1:] == '''
!BEGINSOURCE <cStringIO.StringI object at 0x1518de0> mode=free90
  !comment line 1

  !comment line 2
  MODULE foo
    !comment line 3
    SUBROUTINE f()
      !comment line 4
    END SUBROUTINE f
    !comment line 5
  END MODULE foo
'''.strip().split('\n')[1:]

    assert tree.asfix().strip().split('\n')[1:]=='''
C      BEGINSOURCE <cStringIO.StringI object at 0x1630de0> mode=free90
C       comment line 1

C       comment line 2
        MODULE foo
C         comment line 3
          SUBROUTINE f()
C           comment line 4
          END SUBROUTINE f
C         comment line 5
        END MODULE foo
'''.strip().split('\n')[1:]

def test_labels():
    source_str = '''\
subroutine foo
  real a
! Valid code:
100 a = 3
  l: do
  end do l
200 &! haa
   a=4
300 l1: do
  end do l1
end subroutine foo
'''
    tree = parse(source_str, isfree=True, isstrict=False,
                 ignore_comments=False)
    assert str(tree).strip().split('\n')[1:]=='''
!BEGINSOURCE <cStringIO.StringI object at 0x2952e70> mode=free90
  SUBROUTINE foo()
    REAL a
    ! Valid code:
100 a = 3
    l: DO
    END DO l
200 a = 4
    ! haa
300 l1: DO
    END DO l1
  END SUBROUTINE foo
'''.strip().split('\n')[1:]

    source_str = '''\
      subroutine foo
      real a
      ! Valid code:
  100 a = 3
      l: do
      end do l
  200 ! haa
     &a=4
  300 l1: do
      end do l1
      end subroutine foo
'''
    tree = parse(source_str, isfree=False, isstrict=False,
                 ignore_comments=False)
    assert str(tree).strip().split('\n')[1:]=='''
!      BEGINSOURCE <cStringIO.StringI object at 0x1d3b390> mode=fix90
        SUBROUTINE foo()
          REAL a
          ! Valid code:
 100      a = 3
          l: DO
          END DO l
 200      a = 4
          ! haa
 300      l1: DO
          END DO l1
        END SUBROUTINE foo
'''.strip().split('\n')[1:]
