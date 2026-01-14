
import { useEffect, useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const About = () => {
    return (
        <div className="min-h-screen flex flex-col">
            <Header />

            <main className="flex-1 container mx-auto px-4 py-8 flex items-center justify-center">
                <div className="text-center max-w-2xl mx-auto p-12 rounded-lg border bg-card shadow-sm">
                    <h1 className="text-4xl md:text-6xl font-bold text-primary mb-6">Coming Soon</h1>
                    <p className="text-xl text-muted-foreground">
                        Halaman Tentang Kami sedang dalam tahap pengembangan.
                        <br />
                        Silakan kembali lagi nanti.
                    </p>
                </div>
            </main>

            <Footer />
        </div>
    );
};

export default About;
