"use client";

import React, { useState } from "react";

interface EstimateFormProps {
    onSubmit: (description: string) => void;
    isLoading?: boolean;

}

export default function EstimateForm({
    onSubmit,
    isLoading = false,
}: EstimateFormProps) {
    const [description, setDescription] = useState<string>("");

}