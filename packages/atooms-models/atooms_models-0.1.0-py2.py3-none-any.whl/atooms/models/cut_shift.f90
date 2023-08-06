module cutoff

  implicit none

  double precision, allocatable :: rcut_(:,:)
  double precision, allocatable :: ucut(:,:)

contains

  subroutine setup(rcut)
    double precision, intent(in) :: rcut(:,:)
    if (allocated(rcut_)) return
    allocate(rcut_(size(rcut,1),size(rcut,2)), source=rcut)
  end subroutine setup

  subroutine is_zero(isp,jsp,rsq,result)
    integer,          intent(in) :: isp, jsp
    double precision, intent(in) :: rsq
    logical,          intent(out) :: result
    result = rsq > rcut_(isp,jsp)**2
  end subroutine is_zero

  subroutine tailor(potential)
    integer :: isp,jsp,nsp
    double precision :: rcutsq, u, w, h, uu(3)
    INTERFACE
       subroutine compute(isp,jsp,rsq,u,w,h)
         integer,          intent(in)  :: isp, jsp
         double precision, intent(in)  :: rsq
         double precision, intent(inout) :: u, w, h
       END SUBROUTINE compute
    END INTERFACE
    procedure(compute) :: potential
    nsp = size(rcut_)
    if (allocated(ucut)) return
    allocate(ucut(nsp,nsp))
    do isp = 1,nsp
       do jsp = 1,nsp
          rcutsq = rcut_(isp,jsp)**2
          ! signature is not guessed correctly, u, w, h are intent(in)
          call potential(isp,jsp,rcutsq,ucut(isp,jsp),w,h)
       end do
    end do
  end subroutine tailor

  subroutine smooth(isp,jsp,rsq,uij,wij,hij)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq  ! unused
    double precision, intent(inout) :: uij,wij,hij
    uij = uij - ucut(isp,jsp)
    wij = wij ! unused
    hij = hij ! unused
  end subroutine smooth
  
end module cutoff
