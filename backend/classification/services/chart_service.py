from django.conf import settings

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os
import uuid


class ChartService:

    @staticmethod
    def generate_confusion_matrix(confusion_matrix):

        plt.figure(figsize=(5, 4))

        plt.imshow(
            confusion_matrix,
            interpolation="nearest",
        )

        plt.title("Confusion Matrix")

        plt.colorbar()

        labels = ["0", "1"]

        plt.xticks(np.arange(len(labels)), labels)
        plt.yticks(np.arange(len(labels)), labels)

        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")

        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix[0])):
                plt.text(
                    j,
                    i,
                    str(confusion_matrix[i][j]),
                    ha="center",
                    va="center",
                )

        # Create media/img if it doesn't exist
        img_dir = os.path.join(settings.MEDIA_ROOT, "img")
        os.makedirs(img_dir, exist_ok=True)

        filename = f"confusion_matrix_{uuid.uuid4().hex}.png"

        chart_path = os.path.join(
            img_dir,
            filename,
        )

        plt.savefig(chart_path, bbox_inches="tight")
        plt.close()

        return f"img/{filename}"