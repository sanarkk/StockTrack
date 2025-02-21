import React, {useEffect, useState} from "react";
import styles from "./LoginPage.module.scss";
import PasswordEye from "heroicons/24/solid/eye.svg"
import CrossedPasswordEye from "heroicons/24/solid/eye-slash.svg"
import useDeviceDetect from "../../useDeviceDetect";
import {Link} from "react-router";


const LoginPage = () => {
    const [activeButton, setActiveButton] = useState("login");
    const [wantToRegister, setWantToRegister] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [secondPassword, setSecondPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const {isDeviceSmall} = useDeviceDetect('md');


    const switchToLogin = () => {
        setWantToRegister(false);
        setActiveButton("login");
        setShowPassword(false)
        setUsername("")
        setPassword("")
        setSecondPassword("")
    }

    const switchToRegister = () => {
        setWantToRegister(true);
        setActiveButton("register");
        setShowPassword(false)
        setUsername("")
        setPassword("")
        setSecondPassword("")
    }

    //Password validation
    useEffect(() => {
        if (password !== secondPassword && secondPassword !== "") {
            setErrorMessage("Passwords do not match");
        } else {
            setErrorMessage("");
        }
    }, [password, secondPassword]);

    return (
        <div className={styles.wrapper}>
            <div className={styles["welcome-section"]}>
                <div className={styles.title}>
                    <p>Welcome to StockTrack</p>
                </div>
                {!isDeviceSmall && (
                    <div className={styles.text}>
                        <p>If you love having all your important info in one place, you need to join us!</p>
                        <p>We keep you on track with everything you need, all in one convenient spot on our website.</p>
                    </div>
                )}
            </div>
            {wantToRegister ? (
                <div className={styles["register-form"]}>
                    <div className={styles["register-wrapper"]}>
                        <div className={styles["switch-buttons"]}>
                            <button
                                className={activeButton === "login" ? styles.clicked : ""}
                                onClick={switchToLogin}
                            >
                                Login
                            </button>
                            <div className={styles.bar}></div>
                            <button
                                className={activeButton === "register" ? styles.clicked : ""}
                                onClick={switchToRegister}
                            >
                                Register
                            </button>
                        </div>
                        <form className={styles['register-inputs']}>
                            <div className={styles['username-input']}>
                                <p className={styles['input-label']}>Username</p>
                                <input className={styles.input} onChange={(e) => setUsername(e.target.value)}
                                       value={username} placeholder="Enter your username" type="text"/>
                            </div>
                            <br/>
                            <div className={styles['password-input']}>
                                <p className={styles['input-label']}>Password</p>
                                <input className={styles.input} onChange={(e) => setPassword(e.target.value)}
                                       value={password} placeholder="Enter your password"
                                       type={showPassword ? "text" : "password"}/>
                            </div>
                            <br/>
                            <div className={styles['password-input']}>
                                <p className={styles['input-label']}>Password</p>
                                <input className={styles.input} onChange={(e) => setSecondPassword(e.target.value)}
                                       value={secondPassword} placeholder="Enter your password"
                                       type={showPassword ? "text" : "password"}/>
                            </div>
                            <button type="button" onClick={() => setShowPassword(!showPassword)}
                                    className={styles['show-password-btn']}>
                                {showPassword ? (
                                    <img src={CrossedPasswordEye} alt="Crossed Password eye"/>
                                ) : (
                                    <img src={PasswordEye} alt="Password eye"/>
                                )}
                            </button>
                            <p className={styles['error-message']}>{errorMessage}</p>
                        </form>
                        <div className={styles['submit-btn-container']}>
                            <button className={styles['submit-btn']}>
                                Register
                            </button>
                        </div>
                    </div>
                </div>
            ) : (
                <div className={styles["login-form"]}>
                    <div className={styles["login-wrapper"]}>
                        <div className={styles["switch-buttons"]}>
                            <button
                                className={activeButton === "login" ? styles.clicked : ""}
                                onClick={switchToLogin}
                            >
                                Login
                            </button>
                            <div className={styles.bar}></div>
                            <button
                                className={activeButton === "register" ? styles.clicked : ""}
                                onClick={switchToRegister}
                            >
                                Register
                            </button>
                        </div>
                        <form className={styles.inputs}>
                            <div className={styles['username-input']}>
                                <p className={styles['input-label']}>Username</p>
                                <input className={styles.input} onChange={(e) => setUsername(e.target.value)}
                                       value={username} placeholder="Enter your username" type="text"/>
                            </div>
                            <div className={styles['password-input']}>
                                <p className={styles['input-label']}>Password</p>
                                <input className={styles.input} onChange={(e) => setPassword(e.target.value)}
                                       value={password} placeholder="Enter your password"
                                       type={showPassword ? "text" : "password"}/>
                                <button type="button" onClick={() => setShowPassword(!showPassword)}
                                        className={styles['show-password-btn']}>
                                    {showPassword ? (
                                        <img src={CrossedPasswordEye} alt="Crossed Password eye"/>
                                    ) : (
                                        <img src={PasswordEye} alt="Password eye"/>
                                    )}
                                </button>
                            </div>
                            <div className={styles['submit-btn-container']}>
                                <button className={styles['submit-btn']}>
                                    Login
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
        ;
};

export default LoginPage;
