// // import { BrowserRouter } from "react-router-dom";
// // import Header from "./components/header/Header";
// // import Footer from "./components/footer/Footer";
// // import AppRouter from "./router/AppRouter";

// // export default function App() {
// //   return (
// //     <BrowserRouter>
// //       <div className="min-h-screen flex flex-col bg-gray-50">
// //         <Header />
// //         <main className="flex-1">
// //           <AppRouter />
// //         </main>
// //         <Footer />
// //       </div>
// //     </BrowserRouter>
// //   );
// // }


// import { BrowserRouter } from "react-router-dom";
// import Header from "./components/header/Header";
// import Footer from "./components/footer/Footer";
// import AppRouter from "./router/AppRouter";

// export default function App() {
//   return (
//     <BrowserRouter>
//       <div className="min-h-screen flex flex-col bg-gray-50">
//         <Header />

//         {/* Main content area */}
//         <main className="flex-1 flex justify-center">
//           <AppRouter />
//         </main>

//         <Footer />
//       </div>
//     </BrowserRouter>
//   );
// }

import { BrowserRouter, useLocation } from "react-router-dom";
import Header from "./components/header/Header";
import Footer from "./components/footer/Footer";
import AppRouter from "./router/AppRouter";

function Layout() {
  const location = useLocation();
  const isChatPage = location.pathname.startsWith("/chat");

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {!isChatPage && <Header />}

      <main className="flex-1 flex justify-center">
        <AppRouter />
      </main>

      {!isChatPage && <Footer />}
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}
