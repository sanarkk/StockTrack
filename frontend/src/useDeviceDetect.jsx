import { useState, useEffect, useLayoutEffect } from 'react';

type DeviceDetectBreakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

const breakpoints: Record<DeviceDetectBreakpoint, number> = {
  xs: 575.98,
  sm: 767.98,
  md: 991.98,
  lg: 1199.98,
  xl: 1599.98,
};

const useDeviceDetect = (breakpoint: DeviceDetectBreakpoint = 'md') => {
  const [isDeviceSmall, setIsDeviceSmall] = useState(false);
  const [isServer, setIsServer] = useState(true);

  const handleUpdateDevice = (): void => {
    setIsServer(false);
    setIsDeviceSmall(window.innerWidth < breakpoints[breakpoint]);
  };

  useLayoutEffect(handleUpdateDevice);

  useEffect(() => {
    window.addEventListener('resize', handleUpdateDevice);
    return () => window.removeEventListener('resize', handleUpdateDevice);
  }, []);

  return {
    isDeviceSmall,
    isDeviceLarge: !isDeviceSmall,
    isServer,
  };
};

export default useDeviceDetect;
