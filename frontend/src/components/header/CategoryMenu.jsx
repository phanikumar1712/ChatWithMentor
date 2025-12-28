// import { useNavigate } from "react-router-dom";

// export default function CategoryMenu() {
//   const navigate = useNavigate();

//   const goToCategory = (category) => {
//     navigate(`/mentors?category=${category}`);
//   };

//   return (
//     <div className="relative group">
//       <button className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition">
//         Categories
//       </button>

//       <div className="absolute left-0 mt-3 w-52 rounded-xl bg-white shadow-lg border
//                       opacity-0 invisible group-hover:opacity-100 group-hover:visible
//                       transition-all duration-200">
//         <ul className="py-2 text-sm">
//           <li onClick={() => goToCategory("spiritual")}
//               className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
//             Spiritual Guides
//           </li>
//           <li onClick={() => goToCategory("scientist")}
//               className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
//             Scientists
//           </li>
//           <li onClick={() => goToCategory("freedom")}
//               className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
//             Freedom Fighters
//           </li>
//           <li onClick={() => goToCategory("leader")}
//               className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
//             Leaders
//           </li>
//         </ul>
//       </div>
//     </div>
//   );
// }


import { useNavigate } from "react-router-dom";

export default function CategoryMenu() {
  const navigate = useNavigate();

  const goToCategory = (category) => {
    navigate(`/mentors?category=${category}`);
  };

  return (
    <div className="relative group">
      <button className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition">
        Categories
      </button>

      <div className="absolute left-0 mt-3 w-52 rounded-xl bg-white shadow-lg border
                      opacity-0 invisible group-hover:opacity-100 group-hover:visible
                      transition-all duration-200">
        <ul className="py-2 text-sm">
          <li
            onClick={() => goToCategory("spiritual")}
            className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
            Spiritual Guides
          </li>

          <li
            onClick={() => goToCategory("scientist")}
            className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
            Scientists
          </li>

          <li
            onClick={() => goToCategory("freedom")}
            className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
            Freedom Fighters
          </li>

          {/* <li
            onClick={() => goToCategory("warrior")}
            className="px-4 py-2 cursor-pointer hover:bg-indigo-50">
            Warrior Kings
          </li> */}
        </ul>
      </div>
    </div>
  );
}
