import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# Example feedback scores
feedback_scores = np.array([8.9, 8.86, 8.76, 8.75, 8.9, 9.07, 8.75, 8.71, 8.71, 9.06, 8.76, 9, 9.06, 9, 9.06, 9, 8.89, 9, 8.88, 8.94, 8.47, 8, 8.11, 8.22, 8.22, 8.44, 8.33, 8.22, 9.48, 9.3, 8.9, 9.05, 9.29, 9.33, 9.4])

# Normalize the data to range [0, 1]
normalized_scores = (feedback_scores - feedback_scores.min()) / (feedback_scores.max() - feedback_scores.min())

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

model = Autoencoder()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Convert data to PyTorch tensors
data = torch.tensor(normalized_scores, dtype=torch.float32).view(-1, 1)

# Training the autoencoder
num_epochs = 1000
losses = []
for epoch in range(num_epochs):
    output = model(data)                   
    loss = criterion(output, data)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    losses.append(loss.item())
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Calculate reconstruction error
with torch.no_grad():
    reconstructed = model(data)
    reconstruction_error = torch.mean((reconstructed - data) ** 2, dim=1)

# Determine threshold for anomaly detection (mean + 2 * std is a common choice)
threshold = reconstruction_error.mean() + 2 * reconstruction_error.std()
print(f'Threshold: {threshold}')

# Detect anomalies
anomalies = reconstruction_error > threshold
anomaly_indices = anomalies.nonzero(as_tuple=True)[0]

# Visualizations
plt.figure(figsize=(14, 7))

# Plot original scores
plt.subplot(2, 2, 1)
plt.plot(feedback_scores, 'b-', label='Original Scores')
plt.xlabel('Index')
plt.ylabel('Feedback Score')
plt.title('Original Feedback Scores')
plt.legend()

# Plot normalized scores
plt.subplot(2, 2, 2)
plt.plot(normalized_scores, 'g-', label='Normalized Scores')
plt.xlabel('Index')
plt.ylabel('Normalized Score')
plt.title('Normalized Feedback Scores')
plt.legend()

# Plot reconstruction error
plt.subplot(2, 2, 3)
plt.plot(reconstruction_error.numpy(), 'r-', label='Reconstruction Error')
plt.axhline(y=threshold.item(), color='k', linestyle='--', label='Threshold')
plt.xlabel('Index')
plt.ylabel('Reconstruction Error')
plt.title('Reconstruction Error')
plt.legend()

# Highlight anomalies
plt.subplot(2, 2, 4)
plt.plot(feedback_scores, 'b-', label='Original Scores')
plt.scatter(anomaly_indices.numpy(), feedback_scores[anomaly_indices], color='r', label='Anomalies', zorder=5)
plt.xlabel('Index')
plt.ylabel('Feedback Score')
plt.title('Anomalies in Feedback Scores')
plt.legend()

plt.tight_layout()
plt.show()

print("Anomalies detected at indices:", anomaly_indices.numpy())
print("Anomalous feedback scores:", feedback_scores[anomaly_indices])
