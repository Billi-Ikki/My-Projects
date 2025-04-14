// Group Members
// 22i-1636 (M Bilal Ikram)
// 22i-1697 (Saif-Ur-Rehman)
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0); // Scroll to the top of the page
  }, [pathname]); // Runs whenever the pathname changes

  return null; // This component does not render anything
}

export default ScrollToTop;