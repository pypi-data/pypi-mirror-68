module potential

  implicit none

  double precision, allocatable :: epsilon_(:,:)
  double precision, allocatable :: sigma_(:,:)
  integer :: exponent_

contains

  subroutine setup(exponent, epsilon, sigma)
    integer, intent(in) :: exponent
    double precision, intent(in) :: epsilon(:,:), sigma(:,:)
    if (allocated(epsilon_).and.allocated(sigma_)) return
    exponent_ = exponent
    allocate(epsilon_(size(epsilon,1),size(epsilon,2)), source=epsilon)
    allocate(sigma_(size(sigma,1),size(sigma,2)), source=sigma)
  end subroutine setup
  
  subroutine compute(isp,jsp,rsq,u,w,h)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq
    double precision, intent(inout) :: u, w, h
    u = epsilon_(isp,jsp) * (sigma_(isp,jsp)**2 / rsq)**(exponent_/2)
    w = exponent_ * u / rsq
    h = exponent_ * (exponent_+2) * u / (rsq**2)
  end subroutine compute

end module potential
