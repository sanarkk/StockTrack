import React, { useState, useEffect, useRef } from "react";
import styles from "./SortByDateDropdowm.module.scss";
import DropDownIcon from "../../../assets/icons/dropdownIcon.png";

const SortByDateDropdown = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedOption, setSelectedOption] = useState("Sort by date");
    const dropdownRef = useRef(null);

    const toggleDropdown = () => {
        setIsOpen((prev) => !prev);
    };

    const handleOptionClick = (option) => {
        setSelectedOption(option);
        setIsOpen(false); // Close dropdown after selection
    };

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <div className={styles.dropdown} ref={dropdownRef}>
            <button onClick={toggleDropdown} className={styles["dropdown-btn"]}>
                {selectedOption}
                <img src={DropDownIcon} alt="Dropdown Icon"/>
            </button>
            {isOpen && (
                <ul className={styles["dropdown-menu"]}>
                    {["Newest to latest", "Latest to newest"].map((option) => (
                        <li
                            key={option}
                            className={styles["dropdown-item"]}
                            onClick={() => handleOptionClick(option)}
                        >
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default SortByDateDropdown;
