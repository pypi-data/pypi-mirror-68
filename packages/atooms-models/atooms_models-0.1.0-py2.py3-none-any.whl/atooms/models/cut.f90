module cutoff

  implicit none

  integer, private, parameter :: dp = selected_real_kind(12)
  double precision, allocatable :: rcut_(:,:)

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
    result = rsq >= rcut_(isp,jsp)**2
  end subroutine is_zero
  
  subroutine tailor(potential)
    integer :: isp,jsp,nsp
    double precision :: rcutsq, u, w, h, uu(3)
    procedure() :: potential
  end subroutine tailor

  subroutine smooth(isp,jsp,rsq,uij,wij,hij)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq
    double precision, intent(inout) :: uij,wij,hij
  end subroutine smooth
  
end module cutoff
