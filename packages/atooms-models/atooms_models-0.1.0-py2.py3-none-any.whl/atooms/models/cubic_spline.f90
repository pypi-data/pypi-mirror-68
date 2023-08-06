module cutoff

  implicit none

  double precision, allocatable :: rspl_(:,:)
  double precision, allocatable :: rcut(:,:)
  double precision, allocatable :: acut(:,:)
  double precision, allocatable :: ccut(:,:)

contains

  subroutine setup(rspl)
    double precision, intent(in) :: rspl(:,:)
    if (allocated(rspl_)) return
    allocate(rspl_(size(rspl,1),size(rspl,2)), source=rspl)
  end subroutine setup

  subroutine is_zero(isp,jsp,rsq,result)
    integer,          intent(in) :: isp, jsp
    double precision, intent(in) :: rsq
    logical,          intent(out) :: result
    result = rsq > rcut(isp,jsp)**2
  end subroutine is_zero

  subroutine tailor(potential)
    integer :: isp,jsp,nsp
    double precision :: rsplsq, u, w, h, u1, u2
    !double precision :: potential
    !external :: potential
    INTERFACE
       subroutine compute(isp,jsp,rsq,u,w,h)
         integer,          intent(in)  :: isp, jsp
         double precision, intent(in)  :: rsq
         double precision, intent(inout) :: u, w, h
       END SUBROUTINE compute
    END INTERFACE
    procedure(compute) :: potential
    nsp = size(rspl_,1)
    if (allocated(rcut)) return; allocate(rcut(nsp,nsp))
    if (allocated(acut)) return; allocate(acut(nsp,nsp))
    if (allocated(ccut)) return; allocate(ccut(nsp,nsp))
    do isp = 1,nsp
       do jsp = 1,nsp
          rsplsq = rspl_(isp,jsp)**2
          ! signature is not guessed correctly, u, w, h are intent(in)
          call potential(isp,jsp,rsplsq,u,w,h)
          ! the potential is cubic-splined between rspl < r < rcut 
          ! cubic-splined cutoff : u(r) = A*(B-r)^3 + C for rspl < r < rcut=B
          ! where 
          !   A = - u2^2/(12*u1)
          !   B = rspl - 2*(u1/u2) = rcut
          !   C = u0 + (2*u1^2)/(3*u2)
          ! with u0=u(rspl), u1=u'(rspl), u2=u''(rspl)
          u2 = h * rspl_(isp,jsp)**2 - w ! second order derivative
          u1 = - w * rspl_(isp,jsp)      ! first order derivative
          ccut(isp,jsp) = - u + (2*u1**2) / (3*u2)          
          acut(isp,jsp) = - u2**2 / (12*u1)
          rcut(isp,jsp) = rspl_(isp,jsp) - (2*u1/u2)
       end do
    end do
  end subroutine tailor

  subroutine smooth(isp,jsp,rsq,uij,wij,hij)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq  ! unused
    double precision, intent(inout) :: uij,wij,hij
    double precision :: rij, dr
    ! Cubic splined between rspl and rcut :
    ! function is overwritten when between rspl and rcut
    uij = uij + ccut(isp,jsp)
    IF (rsq > rspl_(isp,jsp)**2) THEN
       rij = sqrt(rsq)
       dr  = rcut(isp,jsp) - rij
       uij = acut(isp,jsp) * dr**3 
       wij = 3.0d0 * acut(isp,jsp) * dr**2 / rij
       ! remember : hij = wij / r^2 + V'' / r^2
       hij = wij / rsq + 6.0d0 * acut(isp,jsp) * dr / rsq
    END IF
  end subroutine smooth
  
end module cutoff
